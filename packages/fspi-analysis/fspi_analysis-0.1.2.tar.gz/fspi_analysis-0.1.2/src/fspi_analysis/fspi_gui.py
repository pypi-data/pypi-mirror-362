import napari
from magicgui import magicgui, widgets 
from skimage import data, io, filters, color, util
import os
from magicgui.widgets import PushButton, Container, FloatSlider, IntSlider, Label, FloatSpinBox, SpinBox 
import pathlib
import traceback
import pandas as pd
from datetime import datetime
import numpy as np
from qtpy.QtCore import QTimer



# --- Global variables 
last_loaded_directory = None
last_loaded_stem = None
status_label = widgets.Label(value="Welcome! Load an image to start.")
path_min_y = None
path_max_y = None
path_y_difference = None
confirmed_y_depth = None # This will store the user-confirmed Y value
depth_line_layer_name = 'depth_selection_line'
depth_slider = IntSlider(value=100, min=0, max=200, label="Depth (Y):", visible=False) 
confirm_depth_button = PushButton(text="Confirm Depth Y", visible=False)
determine_depth_button = PushButton(text="Determine Custom Depth")
threshold_value_widget = FloatSlider(value=0.5, min=0.0, max=1.0, step=0.005, label="Threshold:")
real_core_size_widget = FloatSpinBox(value=6, min=0.001, max = 1000, step=1, label="Real Core Size (cm):")
core_width_px_widget = SpinBox(value=671, min=1, max = 10000, step=1, label="Core Width (px):       ")
_preview_cache = {"gray_image": None, "source_data_id": None, "source_layer_name": None}
viewer = napari.current_viewer() 

# Global timer instance - used for debouncing live preview updates of the threshold
_preview_debounce_timer = QTimer()
_preview_debounce_timer.setSingleShot(True)
_preview_debounce_timer.setInterval(80) ## Adjust this value to control the debounce delay (in milliseconds)


# --- align_image_to_path function (stores path Y stats) ---
def align_image_to_path(image_layer, shapes_layer, viewer):
    global path_y_difference
    if not image_layer: status_label.value = "ERROR: Image layer not found for alignment."; return False
    if not shapes_layer: status_label.value = "ERROR: Shapes layer not found for alignment."; return False
    try:
        original_image = image_layer.data; H, W = original_image.shape[:2]
        if not shapes_layer.data: status_label.value = "No alignment path drawn."; return False
        last_path_data_for_stats = None; last_path_data_for_alignment = None
        for i in range(len(shapes_layer.data) - 1, -1, -1):
            current_shape_type_list_or_str = shapes_layer.shape_type; actual_shape_type = ''
            if isinstance(current_shape_type_list_or_str, list):
                if i < len(current_shape_type_list_or_str): actual_shape_type = current_shape_type_list_or_str[i]
                else: continue
            else: actual_shape_type = current_shape_type_list_or_str
            if actual_shape_type == 'path':
                if i < len(shapes_layer.data):
                    last_path_data_for_alignment = shapes_layer.data[i]
                    last_path_data_for_stats = shapes_layer.data[i] 
                    break
        if last_path_data_for_alignment is None: status_label.value = "No 'path' shape found for alignment."; return False
        if last_path_data_for_alignment.shape[1] != 2 or last_path_data_for_alignment.shape[0] < 1: status_label.value = "Path data is invalid."; return False
        if last_path_data_for_stats is not None and last_path_data_for_stats.shape[0] > 0:
            path_y_coords = last_path_data_for_stats[:, 0]
            global path_min_y, path_max_y, path_y_difference
            path_min_y = float(np.min(path_y_coords)); path_max_y = float(np.max(path_y_coords))
            path_y_difference = path_max_y - path_min_y
        else: path_min_y, path_max_y, path_y_difference = None, None, None
        polyline_coords = last_path_data_for_alignment; sorted_indices = np.argsort(polyline_coords[:, 1])
        px_sorted, py_sorted = polyline_coords[sorted_indices, 1], polyline_coords[sorted_indices, 0]
        unique_px, unique_indices = np.unique(px_sorted, return_index=True); unique_py = py_sorted[unique_indices]
        if unique_px.size == 0 : status_label.value = "No valid points for interpolation."; return False
        if unique_px.size < 2:
            if unique_px.size == 1: y_val_for_all_cols = np.mean(py_sorted); interpolated_y_line = np.full(W, y_val_for_all_cols)
            else: status_label.value = "Not enough unique x-points for alignment path."; return False
        else: interpolated_y_line = np.interp(np.arange(W), unique_px, unique_py)
        if original_image.ndim == 3 and original_image.shape[-1] > 1: aligned_image = np.zeros_like(original_image)
        else: aligned_image = np.zeros_like(original_image)
        for x_col in range(W):
            y_line_at_x = int(round(interpolated_y_line[x_col])); y_line_at_x_clipped = np.clip(y_line_at_x, 0, H - 1)
            pixels_to_crop_from_top = y_line_at_x_clipped; num_pixels_to_keep = H - pixels_to_crop_from_top
            if num_pixels_to_keep > 0:
                source_start_y, source_end_y = pixels_to_crop_from_top, H
                dest_start_y, dest_end_y = 0, num_pixels_to_keep
                if original_image.ndim == 2: aligned_image[dest_start_y:dest_end_y, x_col] = original_image[source_start_y:source_end_y, x_col]
                elif original_image.ndim == 3: aligned_image[dest_start_y:dest_end_y, x_col, :] = original_image[source_start_y:source_end_y, x_col, :]
        try:
            aligned_layer = viewer.layers['aligned_image']; aligned_layer.data = aligned_image
            aligned_layer.contrast_limits = image_layer.contrast_limits; aligned_layer.colormap = image_layer.colormap
            aligned_layer.blending = image_layer.blending; aligned_layer.visible = True
        except KeyError:
            viewer.add_image(aligned_image, name='aligned_image', colormap=image_layer.colormap.name,
                             contrast_limits=image_layer.contrast_limits, blending=image_layer.blending)
        num_points_in_path = 0
        if last_path_data_for_stats is not None : num_points_in_path = last_path_data_for_stats.shape[0]
        message = f"Image aligned. Path Y range: [{path_min_y:.1f}-{path_max_y:.1f}]." if path_min_y is not None else "Image aligned."
        status_label.value = message
         # --- NEW: Invalidate preview cache after alignment ---
        _preview_cache["gray_image"] = None
        _preview_cache["source_data_id"] = None
        _preview_cache["source_layer_name"] = None
        # ----------------------------------------------------
        return True
    except Exception as e: status_label.value = f"ERROR during alignment: {e}"; traceback.print_exc(); return False


def clear_alignment_paths():
    try:
        shapes_layer = viewer.layers['alignment_path']; shapes_layer.data = []
        status_label.value = "Alignment paths cleared."
    except (NameError, KeyError): status_label.value = "Could not find alignment_path layer to clear."
    except Exception as e: status_label.value = f"Error clearing paths: {e}"

@magicgui(call_button="Load Image File", image_path={"label": "Choose Image:", "mode": "r"})
def load_new_image(image_path: pathlib.Path):
    global last_loaded_directory, last_loaded_stem
    reset_viewer_state(called_internally=True) 
    if not image_path or not image_path.is_file(): status_label.value = "No valid file selected."; return
    status_label.value = f"Loading: {image_path.name}..."
    try:
        loaded_image_data = io.imread(image_path); original_layer_name = 'original_image'
        try:
            original_layer = viewer.layers[original_layer_name]; original_layer.data = loaded_image_data
            original_layer.reset_contrast_limits()
        except KeyError:
            original_layer = viewer.add_image(loaded_image_data, name=original_layer_name)
            original_layer.reset_contrast_limits()
        last_loaded_directory = image_path.parent; last_loaded_stem = image_path.stem
        shapes_layer_name = 'alignment_path'
        try:
            shapes_layer_index = viewer.layers.index(shapes_layer_name); target_index = len(viewer.layers) - 1
            if shapes_layer_index != target_index: viewer.layers.move(shapes_layer_index, target_index)
        except (ValueError, KeyError): pass 
        status_label.value = f"Loaded: {image_path.name}. Viewer reset."
        MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB
        file_size_bytes = os.path.getsize(image_path)
        if file_size_bytes > MAX_FILE_SIZE_BYTES:
            status_label.value = f"File is very large ({file_size_bytes / (1024*1024):.2f} MB) so analysis may be slow. Are you sure your images are not corrupted?"
    except Exception as e: status_label.value = f"Error loading {image_path.name}: {e}"; traceback.print_exc()

def _get_thresholdable_gray_image(source_image_layer):
    if source_image_layer is None: return None
    image_data = source_image_layer.data; gray_image = None
    try:
        if image_data.ndim == 3 and image_data.shape[-1] in [3, 4]:
            img_float = util.img_as_float(image_data[...,:3]); gray_image = color.rgb2gray(img_float)
        elif image_data.ndim == 2:
            if np.issubdtype(image_data.dtype, np.integer): gray_image = util.img_as_float(image_data)
            elif image_data.min() >= 0 and image_data.max() <= 1: gray_image = image_data
            else:
                 min_val, max_val = np.min(image_data), np.max(image_data)
                 if max_val > min_val: gray_image = (image_data - min_val) / (max_val - min_val)
                 else: gray_image = np.zeros_like(image_data, dtype=float)
        else: return None
        return gray_image
    except Exception as e: print(f"ERROR in _get_thresholdable_gray_image: {e}"); traceback.print_exc(); return None

def calculate_auto_threshold():
    status_label.value = "Calculating auto threshold..."
    try:
        aligned_layer = viewer.layers['aligned_image']; gray_image = _get_thresholdable_gray_image(aligned_layer)
        if gray_image is not None:
            _preview_cache["gray_image"] = gray_image
            _preview_cache["source_data_id"] = id(aligned_layer.data)
            _preview_cache["source_layer_name"] = aligned_layer.name
            auto_thresh_value = filters.threshold_otsu(gray_image); threshold_value_widget.value = auto_thresh_value
            _update_threshold_preview() 
            try:
                if 'original_image' in viewer.layers: viewer.layers['original_image'].visible = False
                if 'aligned_image' in viewer.layers: viewer.layers['aligned_image'].visible = False
                if 'thresholded_mask' in viewer.layers: viewer.layers['thresholded_mask'].visible = True
            except KeyError: pass
            status_label.value = f"Auto threshold: {auto_thresh_value:.4f}. Layers hidden."
        else: status_label.value = "Could not prepare image for auto threshold."
    except KeyError: status_label.value = "ERROR: 'aligned_image' layer not found. Align first."
    except Exception as e: status_label.value = f"Error in auto threshold: {e}"; traceback.print_exc()

def _update_threshold_preview():
    mask_layer_name = 'thresholded_mask'
    
    try:
        if 'aligned_image' not in viewer.layers:
            _preview_cache["gray_image"] = None # Clear cache if source disappears
            _preview_cache["source_data_id"] = None
            _preview_cache["source_layer_name"] = None
            return

        aligned_layer = viewer.layers['aligned_image']
        current_data_id = id(aligned_layer.data)
        current_layer_name = aligned_layer.name # Could also check name

        gray_image_to_use = None

        if (_preview_cache["source_layer_name"] == current_layer_name and
            _preview_cache["source_data_id"] == current_data_id and 
            _preview_cache["gray_image"] is not None):
            gray_image_to_use = _preview_cache["gray_image"]
            # print("DEBUG: Using cached gray image for preview") # Optional
        else:
            # print("DEBUG: Recalculating gray image for preview") # Optional
            gray_image_to_use = _get_thresholdable_gray_image(aligned_layer)
            if gray_image_to_use is not None:
                _preview_cache["gray_image"] = gray_image_to_use
                _preview_cache["source_data_id"] = current_data_id
                _preview_cache["source_layer_name"] = current_layer_name
            else:
                # Failed to get gray image, clear cache and exit
                _preview_cache["gray_image"] = None
                _preview_cache["source_data_id"] = None
                _preview_cache["source_layer_name"] = None
                status_label.value = "Error: Could not get gray image for preview."
                return

        if gray_image_to_use is not None:
            threshold = threshold_value_widget.value
            binary_mask = gray_image_to_use > threshold
            mask_int = binary_mask.astype(np.uint8)
            
            try:
                mask_layer = viewer.layers[mask_layer_name]
                mask_layer.data = mask_int
            except KeyError:
                viewer.add_labels(mask_int, name=mask_layer_name, visible=True)
            
            if mask_layer_name in viewer.layers:
                 viewer.layers[mask_layer_name].color_mode = 'direct'
                 viewer.layers[mask_layer_name].color = {0: 'transparent', 1: 'yellow'}
                 viewer.layers[mask_layer_name].opacity = 0.6
                 viewer.layers[mask_layer_name].visible = True
    except Exception as e: 
        status_label.value = f"Live preview error: {e}"
        # traceback.print_exc() # Keep for debugging if needed

    mask_layer_name = 'thresholded_mask'
    try:
        if 'aligned_image' not in viewer.layers: return
        aligned_layer = viewer.layers['aligned_image']; gray_image = _get_thresholdable_gray_image(aligned_layer)
        if gray_image is not None:
            threshold = threshold_value_widget.value; binary_mask = gray_image > threshold
            mask_int = binary_mask.astype(np.uint8)
            try:
                mask_layer = viewer.layers[mask_layer_name]; mask_layer.data = mask_int
            except KeyError:
                viewer.add_labels(mask_int, name=mask_layer_name, visible=True)
            if mask_layer_name in viewer.layers:
                 viewer.layers[mask_layer_name].color_mode = 'direct'
                 viewer.layers[mask_layer_name].color = {0: 'transparent', 1: 'yellow'}
                 viewer.layers[mask_layer_name].opacity = 0.6
                 viewer.layers[mask_layer_name].visible = True
    except Exception as e: status_label.value = f"Live preview error: {e}"; traceback.print_exc()

def apply_manual_threshold():
    _update_threshold_preview() 
    if 'thresholded_mask' in viewer.layers:
        status_label.value = f"Threshold {threshold_value_widget.value:.4f} applied. Mask updated."
    elif 'aligned_image' not in viewer.layers:
        status_label.value = "Cannot apply: 'aligned_image' layer not found."
    else:
        status_label.value = "Mask layer could not be created/updated."

def process_and_save():
    global viewer, last_loaded_directory, last_loaded_stem, status_label
    global path_min_y, path_max_y, path_y_difference, confirmed_y_depth, pixel_size_cm_per_px
    status_label.value = "Processing and saving results..."

    if last_loaded_directory is None or last_loaded_stem is None:
        status_label.value = "ERROR: No custom image loaded. Load image first."; return
    if 'thresholded_mask' not in viewer.layers:
        status_label.value = "ERROR: 'thresholded_mask' layer not found. Apply threshold first."; return

    try:
        mask_layer = viewer.layers['thresholded_mask']
        mask_data_full = mask_layer.data # This is the full mask
        H_full, W = mask_data_full.shape
        if W == 0: status_label.value = "ERROR: Mask width is zero."; return
    except KeyError: status_label.value = "ERROR: Could not access 'thresholded_mask' data."; return
    except Exception as e: status_label.value = f"ERROR accessing mask data: {e}"; traceback.print_exc(); return

    # --- Save Mask Image (uses full mask_data_full) ---
    try:
        mask_filename = f"{last_loaded_stem}_Mask.png"
        output_mask_path = last_loaded_directory / mask_filename
        mask_to_save = (mask_data_full * 255).astype(np.uint8)
        io.imsave(output_mask_path, mask_to_save, check_contrast=False)
        print(f"Mask image saved to: {output_mask_path}")
    except Exception as e: status_label.value = f"ERROR saving mask image: {e}"; traceback.print_exc(); return

    # --- Calculations (Row sums on full mask, vertical distances on constrained mask) ---
    try:
        profile_filename = f"{last_loaded_stem}_Profile.csv"
        output_profile_path = last_loaded_directory / profile_filename

        # Row sums and relative count from the full mask
        row_sums_full = np.sum(mask_data_full, axis=1)
        depths_full = np.arange(H_full)
        total_sum_of_mask_pixels_full = np.sum(mask_data_full)
        if total_sum_of_mask_pixels_full > 0:
            relative_counts_full = (row_sums_full / total_sum_of_mask_pixels_full) * 100
        else:
            relative_counts_full = np.zeros_like(row_sums_full, dtype=float)

        # --- Vertical Distance Calculation ---
        # Determine the mask to process for vertical distances based on confirmed_y_depth
        mask_for_vertical_distances = mask_data_full # Default to full mask
        effective_H_for_vertical_distances = H_full

        if confirmed_y_depth is not None:
            # Use rows 0 up to AND INCLUDING confirmed_y_depth
            # Ensure confirmed_y_depth is within bounds of the mask
            clamped_depth = min(int(confirmed_y_depth), H_full - 1)
            roi_depth_info_str = f"Up to Y={clamped_depth} (inclusive)" ## For adding into summary text file later  
            if clamped_depth < 0 : # e.g. if confirmed_y_depth was 0, then +1 is 1, slice is :1 (row 0)
                effective_H_for_vertical_distances = 0
            else:
                effective_H_for_vertical_distances = clamped_depth + 1

            mask_for_vertical_distances = mask_data_full[:effective_H_for_vertical_distances, :]
            print(f"Calculating vertical distances within Y range: 0-{clamped_depth} (inclusive)")
        else:
            print("No custom depth set, calculating vertical distances for full height.")


        vertical_distances_roi = []
        if effective_H_for_vertical_distances > 0 and mask_for_vertical_distances.shape[0] > 0 : # Check if there are rows
            for x_col in range(W):
                column_data = mask_for_vertical_distances[:, x_col]
                on_pixels_indices = np.where(column_data == 1)[0]
                if on_pixels_indices.size > 0: # If at least one 'on' pixel
                    topmost_y = np.min(on_pixels_indices)
                    bottommost_y = np.max(on_pixels_indices)
                    distance = bottommost_y - topmost_y + 1 # Includes both ends
                    vertical_distances_roi.append(distance)

        mean_vertical_distance_roi = np.nan
        median_vertical_distance_roi = np.nan
        if vertical_distances_roi:
            mean_vertical_distance_roi = np.mean(vertical_distances_roi)
            median_vertical_distance_roi = np.median(vertical_distances_roi)
            max_vertical_distance_roi = np.max(vertical_distances_roi)
            print(f"Mean Vertical Distance (ROI): {mean_vertical_distance_roi:.2f}")
            print(f"Median Vertical Distance (ROI): {median_vertical_distance_roi:.2f}")
        else:
            print("No vertical distances calculated in ROI (e.g., empty mask region).")
        # ---------------------------------------

         #real_core_size_cm = 0.0
        core_width_in_px = 0.0
        pixel_size_cm_per_px = 0.0
        if real_core_size_widget is not None and core_width_px_widget is not None:
            real_core_size_cm = real_core_size_widget.value
            core_width_in_px = core_width_px_widget.value
            pixel_size_cm_per_px = real_core_size_cm / core_width_in_px
            mean_vertical_distance_scaled = (mean_vertical_distance_roi*pixel_size_cm_per_px)
            median_vertical_distance_scaled = (median_vertical_distance_roi*pixel_size_cm_per_px)
            max_vertical_distance_roi_scaled = (max_vertical_distance_roi*pixel_size_cm_per_px)
            alignment_path_scaled = (path_y_difference * pixel_size_cm_per_px)

        # Create pandas DataFrame
        # The per-row data should match the full height of the mask
        df_data = {
            'Row': depths_full,
            'Row_Sums': row_sums_full,
            'Row_Sum_Relative_Count': relative_counts_full,
            'Surface_Path_Difference_Pixels': path_y_difference if path_y_difference is not None else np.nan,
            'Surface_Path_Difference_cm': alignment_path_scaled if path_y_difference is not None else np.nan,
            'Mean_Depth_Distance_Pixels': mean_vertical_distance_roi,
            'Median_Depth_Distance_Pixels': median_vertical_distance_roi,
            'Max_Depth_Distance_Pixels': max_vertical_distance_roi,
            'Mean_Depth_Distance_cm': mean_vertical_distance_scaled,
            'Median_Depth_Distance_cm': median_vertical_distance_scaled,
            'Max_Depth_Distance_cm': max_vertical_distance_roi_scaled,
            'centimeter_per_Pixel': pixel_size_cm_per_px
        }
        df_columns = ['Row', 'Row_Sums', 'Row_Sum_Relative_Count', 'centimeter_per_Pixel', 'Surface_Path_Difference_Pixels',
                      'Surface_Path_Difference_cm', 'Mean_Depth_Distance_Pixels', 'Median_Depth_Distance_Pixels', 'Max_Depth_Distance_Pixels', 'Mean_Depth_Distance_cm', 'Median_Depth_Distance_cm', 'Max_Depth_Distance_cm']
        df = pd.DataFrame(df_data, columns=df_columns)

        df.to_csv(output_profile_path, index=False, float_format='%.6g')
        status_label.value = f"Mask & profile (with vertical distances) saved for {last_loaded_stem}."
    except Exception as e: status_label.value = f"ERROR saving profile CSV: {e}"; traceback.print_exc()

    try:
        summary_filename = f"{last_loaded_stem}_Summary.txt"
        output_summary_path = last_loaded_directory / summary_filename
        with open(output_summary_path, 'w') as f:
            f.write(f"Image Analysis Summary\n")
            f.write(f"Original File Stem: {last_loaded_stem}\n")
            f.write(f"Processing Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 30 + "\n")
            f.write("Alignment Path Statistics:\n")
            f.write(f"  Path Min Y: {path_min_y:.2f} px\n" if path_min_y is not None else "  Path Min Y: Not available\n")
            f.write(f"  Path Max Y: {path_max_y:.2f} px\n" if path_max_y is not None else "  Path Max Y: Not available\n")
            f.write("-" * 30 + "\n")
            f.write("Scaling Factors:\n")
            f.write(f"  Real Core Size Input: {real_core_size_cm:.3g} cm\n")
            f.write(f"  Core Width Input:  {core_width_in_px:.1g} px\n")
            f.write(f"  Pixel Size Calculated: {pixel_size_cm_per_px:.6g} cm/px\n")
            f.write("-" * 30 + "\n")
            f.write(f"ROI Vertical Distances (Processed Region: {roi_depth_info_str}):\n")

        
            
           
        print(f"Summary data saved to: {output_summary_path}")
        status_label.value = f"Results saved for {last_loaded_stem}."
    except Exception as e: status_label.value = f"ERROR saving summary TXT: {e}"; traceback.print_exc()

def reset_viewer_state(called_internally=False):

    if not called_internally:
        status_label.value = "Resetting viewer state..."
    try:
        if 'aligned_image' in viewer.layers: viewer.layers.remove('aligned_image')
        if 'thresholded_mask' in viewer.layers: viewer.layers.remove('thresholded_mask')
        if depth_line_layer_name in viewer.layers: viewer.layers.remove(depth_line_layer_name)

        if 'original_image' in viewer.layers: viewer.layers['original_image'].visible = True
        clear_alignment_paths() # Keep its own status update or make it fully silent

        if 'depth_slider' in globals() and depth_slider is not None and isinstance(depth_slider, widgets.Widget):
            depth_slider.visible = False
        if 'confirm_depth_button' in globals() and confirm_depth_button is not None and isinstance(confirm_depth_button, widgets.Widget):
            confirm_depth_button.visible = False
        if 'determine_depth_button' in globals() and determine_depth_button is not None and isinstance(determine_depth_button, widgets.Widget):
            determine_depth_button.enabled = True

        _preview_cache["gray_image"] = None
        _preview_cache["source_data_id"] = None
        _preview_cache["source_layer_name"] = None

        if not called_internally:
            status_label.value = "Viewer reset. Ready for next image."
    except Exception as e:
        if not called_internally: status_label.value = f"Error during reset: {e}"
        traceback.print_exc()

# --- Functions for Depth Determination ---
# (start_depth_determination, _update_depth_line, confirm_selected_depth)
def start_depth_determination():
    status_label.value = "Starting depth determination..."
    if 'aligned_image' not in viewer.layers:
        status_label.value = "ERROR: 'aligned_image' layer not found. Align image first."; return
    try:
        aligned_layer = viewer.layers['aligned_image']; H, W = aligned_layer.data.shape[:2]
        if depth_line_layer_name in viewer.layers: viewer.layers.remove(depth_line_layer_name)
        y_initial = H // 2; line_data = np.array([[[y_initial, 0], [y_initial, W-1]]])
        viewer.add_shapes(data=line_data, shape_type='line', edge_color='lime', edge_width= int(H // 300),
                          name=depth_line_layer_name, ndim=2)
        try: 
            idx = viewer.layers.index(depth_line_layer_name); viewer.layers.move(idx, len(viewer.layers)-1)
        except (ValueError, KeyError): pass
        depth_slider.min = 0; depth_slider.max = H - 1; depth_slider.value = y_initial
        depth_slider.visible = True; confirm_depth_button.visible = True
        determine_depth_button.enabled = False 
        status_label.value = "Adjust slider for depth, then click 'Confirm Depth Y'."
    except Exception as e: status_label.value = f"Error starting depth determination: {e}"; traceback.print_exc()

def _update_depth_line():
    try:
        if depth_line_layer_name not in viewer.layers or 'aligned_image' not in viewer.layers: return
        line_layer = viewer.layers[depth_line_layer_name]
        aligned_W = viewer.layers['aligned_image'].data.shape[1]; y_new = depth_slider.value
        line_layer.data = [np.array([[y_new, 0], [y_new, aligned_W]])]
    except Exception as e: status_label.value = f"Error updating depth line: {e}"

def confirm_selected_depth():
    global confirmed_y_depth
    confirmed_y_depth = depth_slider.value
    status_label.value = f"Custom depth Y = {confirmed_y_depth} confirmed."
    print(f"Confirmed Y-depth: {confirmed_y_depth}")
    try:
        if depth_line_layer_name in viewer.layers: viewer.layers.remove(depth_line_layer_name)
    except Exception as e: status_label.value = f"Error removing depth line: {e}"
    depth_slider.visible = False; confirm_depth_button.visible = False
    determine_depth_button.enabled = True

def manual_trigger_button_clicked():
        print("'Align Image' button clicked.")
        current_image_layer, current_shapes_layer = None, None
        try:
            current_image_layer = viewer.layers['original_image']
            current_shapes_layer = viewer.layers['alignment_path']
        except KeyError as e: status_label.value = f"ERROR: {e}"; return
        if current_shapes_layer.data and len(current_shapes_layer.data) > 0:
            align_image_to_path(current_image_layer, current_shapes_layer, viewer)
        else: status_label.value = "No path drawn on 'alignment_path' layer."

_preview_debounce_timer.timeout.connect(_update_threshold_preview) 

def _request_threshold_preview_update():
    global _preview_debounce_timer
    _preview_debounce_timer.start() # This will restart the timer if it's already running


def F_Analysis_widget():
    

    sample_image = data.astronaut()
    image_layer = viewer.add_image(sample_image, name='original_image')
    shapes_layer = viewer.add_shapes(data=None, ndim=2, shape_type='path', edge_width=2,
                                    edge_color='cyan', face_color='transparent', name='alignment_path')
    shapes_layer.mode = 'add_path'
    print("Automatic alignment on draw DEACTIVATED.")

    align_button = PushButton(text="Align Image to Last Path")
    align_button.clicked.connect(manual_trigger_button_clicked)
    clear_paths_button = PushButton(text="Clear Alignment Paths")
    clear_paths_button.clicked.connect(clear_alignment_paths)
    load_image_widget = load_new_image
    load_image_widget.label = " "

    depth_label = Label(value="--- Custom Depth Selection ---")
    depth_slider.changed.connect(_update_depth_line)
    determine_depth_button.clicked.connect(start_depth_determination)
    confirm_depth_button.clicked.connect(confirm_selected_depth)

    threshold_label = Label(value="--- Thresholding ---")
    auto_threshold_button = PushButton(text="Auto Threshold")
    auto_threshold_button.clicked.connect(calculate_auto_threshold)
    apply_threshold_button = PushButton(text="Apply Threshold")
    apply_threshold_button.clicked.connect(apply_manual_threshold)
    threshold_value_widget.changed.connect(_request_threshold_preview_update)

    save_label = Label(value="--- Output ---")
    process_save_button = PushButton(text="Process Image and Save Results") # Renamed for clarity
    process_save_button.clicked.connect(process_and_save)
    reset_button = PushButton(text="Reset for Next Image")
    reset_button.clicked.connect(lambda: reset_viewer_state(called_internally=False))

    control_container = Container(widgets=[
        load_image_widget, Label(value="--- Alignment ---"), align_button, clear_paths_button,
        depth_label, determine_depth_button, depth_slider, confirm_depth_button,
        threshold_label, auto_threshold_button, threshold_value_widget, apply_threshold_button,
        save_label, real_core_size_widget,
        core_width_px_widget, process_save_button, Label(value="--- General ---"), reset_button,
        status_label
    ])
     # Add the container to the viewer
    return control_container
    
    
