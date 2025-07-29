'''
This library performs various calculations to analyse the OOS data.
'''

import numpy as np
from scipy.optimize import leastsq
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import welch

class OOSAnonymisation: # pylint: disable=too-many-arguments, too-many-instance-attributes, too-many-locals
    """
    Processor for Out-Of-Straightness (OOS) pipeline survey and route data.
    Provides methods for cleaning, sectioning, and coordinate normalization.
    """
    def __init__(
            self,
            *,
            route_development,
            route_pipeline_group,
            route_pipeline,
            route_kp_from,
            route_kp_to,
            route_pipeline_section_type,
            route_curve_radius,
            survey_development,
            survey_type,
            survey_pipeline_group,
            survey_pipeline,
            survey_kp,
            survey_easting,
            survey_northing,
        ):
        """
        Initialize an OOSAnonymisation object with route and survey data.

        Parameters
        ----------
        route_development : array-like
            Development identifiers for each route section.
        route_pipeline_group : array-like
            Pipeline group identifiers for each route section.
        route_pipeline : array-like
            Pipeline identifiers for each route section.
        route_kp_from : array-like
            Start KP (kilometer point) for each route section.
        route_kp_to : array-like
            End KP (kilometer point) for each route section.
        route_pipeline_section_type : array-like
            Section type (e.g., 'Straight', 'Curve', etc.) for each route section.
        route_curve_radius : array-like
            Design curve radius for each route section.
        survey_development : array-like
            Development identifiers for each survey point.
        survey_type : array-like
            Survey type for each survey point.
        survey_pipeline_group : array-like
            Pipeline group identifiers for each survey point.
        survey_pipeline : array-like
            Pipeline identifiers for each survey point.
        survey_kp : array-like
            KP (kilometer point) for each survey point.
        survey_easting : array-like
            Easting coordinate for each survey point.
        survey_northing : array-like
            Northing coordinate for each survey point.

        Notes
        -----
        All input arrays are converted to NumPy arrays and stored as attributes. Additional
        attributes for section types, numbers, radii, and modified coordinates are
        initialized as NumPy arrays and will be populated by processing methods.
        """
        self.route_development = np.asarray(route_development, dtype=object)
        self.route_pipeline_group = np.asarray(route_pipeline_group, dtype=object)
        self.route_pipeline = np.asarray(route_pipeline, dtype=object)
        self.route_kp_from = np.asarray(route_kp_from, dtype=float)
        self.route_kp_to = np.asarray(route_kp_to, dtype=float)
        self.route_pipeline_section_type = np.asarray(route_pipeline_section_type, dtype=object)
        self.route_curve_radius = np.asarray(route_curve_radius, dtype=float)
        self.survey_development = np.asarray(survey_development, dtype=object)
        self.survey_type = np.asarray(survey_type, dtype=object)
        self.survey_pipeline_group = np.asarray(survey_pipeline_group, dtype=object)
        self.survey_pipeline = np.asarray(survey_pipeline, dtype=object)
        self.survey_kp = np.asarray(survey_kp, dtype=float)
        self.survey_easting = np.asarray(survey_easting, dtype=float)
        self.survey_northing = np.asarray(survey_northing, dtype=float)
        self.survey_section_type = np.full(
            self.survey_kp.shape[0], '', dtype=object
        )
        self.survey_section_no = np.full(
            self.survey_kp.shape[0], np.nan, dtype=float
        )
        self.survey_feature = np.full(
            self.survey_kp.shape[0], '', dtype=object
        )
        self.survey_design_route_curve_radius = np.full(
            self.survey_kp.shape[0], np.nan, dtype=float
        )
        self.survey_actual_route_curve_radius = np.full(
            self.survey_kp.shape[0], np.nan, dtype=float
        )
        self.survey_section_easting_mod = np.full(
            self.survey_kp.shape[0], np.nan, dtype=float
        )
        self.survey_section_northing_mod = np.full(
            self.survey_kp.shape[0], np.nan, dtype=float
        )
        self.survey_section_kp_mod = np.full(
            self.survey_kp.shape[0], np.nan, dtype=float
        )

    def process(self, anonymise: bool = False):
        """
        Run the OOS processing pipeline.

        Parameters
        ----------
        anonymise : bool, default False
            If True, runs the full anonymisation pipeline (with cleaning and grouping).
            If False, runs only the basic section processing.
        """
        self._add_pipeline_section()
        self._add_feature_labels()
        self._add_design_route_curve_radius()
        self._add_actual_route_curve_radius()
        self._transform_pipeline_section_coordinates()
        if anonymise:
            self._trim_feature_kps()
            self._trim_straight_section_ends()
            self._add_pipeline_group_section()
            self._transform_pipeline_group_section_coordinates()

    def _add_pipeline_section(self):
        """
        Add section type ('Straight' or 'Curve') and section number to each survey point.

        For each survey point, determines if it falls within a non-straight route section (based on
        matching pipeline group, pipeline, and KP range) and adds 'Curve' or 'Straight' to
        self.survey_section_type. Then, adds a unique section number (self.survey_section_no) to
        each continuous section of the same type within each (pipeline group, pipeline, survey type)
        group.

        Updates
        -------
        self.survey_section_type : np.ndarray
            Section type ('Straight' or 'Curve') for each survey point.
        self.survey_section_no : np.ndarray
            Section number for each survey point, incremented for each new section.

        Returns
        -------
        None
        """
        # Build mask for non-straight route sections
        mask = ~np.isin(self.route_pipeline_section_type, ['LBMD', 'PWMD', 'ILT', 'Straight'])
        # Indices of route sections that are not straight
        idxs = np.where(mask)[0]
        mask_curve = np.full(self.survey_kp.shape[0], False)
        for i in idxs:
            cond = (
                (self.survey_development == self.route_development[i]) &
                (self.survey_pipeline_group == self.route_pipeline_group[i]) &
                (self.survey_pipeline == self.route_pipeline[i]) &
                (self.survey_kp >= self.route_kp_from[i]) &
                (self.survey_kp <= self.route_kp_to[i])
            )
            mask_curve = mask_curve | cond
        # Create or update section type array
        section_type = np.full(self.survey_kp.shape[0], 'Straight', dtype=object)
        section_type[mask_curve] = 'Curve'
        self.survey_section_type = section_type

        # Add Section No for each continuous section
        group_keys = [
            self.survey_development, self.survey_type,
            self.survey_pipeline_group, self.survey_pipeline
        ]
        section_no = np.zeros(self.survey_kp.shape[0], dtype=int)
        prev_keys = None
        prev_type = None
        current_section = 0
        for i in range(self.survey_kp.shape[0]):
            keys = tuple(key[i] for key in group_keys)
            curr_type = section_type[i]
            if keys != prev_keys:
                current_section = 1
            elif curr_type != prev_type:
                current_section += 1
            section_no[i] = current_section
            prev_keys = keys
            prev_type = curr_type
        self.survey_section_no = section_no

    def _add_feature_labels(self):
        """
        Adds a new attribute 'survey_feature' to the survey points.
        For each feature (PWMD, LBMD, ILT) in the route, finds the closest survey point
        (matching development, pipeline group, pipeline) in KP and adds the feature name
        at that position.
        All other survey points have an empty string.
        """
        feature_types = ['PWMD', 'LBMD', 'ILT']
        for i, section_type in enumerate(self.route_pipeline_section_type):
            if section_type in feature_types:
                dev = self.route_development[i]
                survey = self.survey_type[i]
                group = self.route_pipeline_group[i]
                pipe = self.route_pipeline[i]
                kp = self.route_kp_from[i]
                # Find matching survey points
                mask = (
                    (self.survey_development == dev) &
                    (self.survey_type == survey) &
                    (self.survey_pipeline_group == group) &
                    (self.survey_pipeline == pipe)
                )
                if not np.any(mask):
                    continue
                kp_survey = self.survey_kp[mask]
                idx_in_mask = np.argmin(np.abs(kp_survey - kp))
                idx = np.where(mask)[0][idx_in_mask]
                self.survey_feature[idx] = section_type

    def _add_design_route_curve_radius(self):
        """
        Add the 'Design Route Curve Radius' from route data to each survey point where the
        section type is 'Curve'.

        For each survey point with section type 'Curve', finds the matching route section (by
        development, pipeline group, pipeline, and KP within [KP From, KP To]) and adds
        the corresponding route curve radius to self.survey_design_route_curve_radius.

        Updates
        -------
        self.survey_design_route_curve_radius : np.ndarray
            Design route curve radii for each survey point (NaN for non-curve points).

        Returns
        -------
        None
        """
        mask_curve = self.survey_section_type == 'Curve'
        for i, _ in enumerate(self.route_development):
            cond = (
                (self.survey_development == self.route_development[i]) &
                (self.survey_pipeline_group == self.route_pipeline_group[i]) &
                (self.survey_pipeline == self.route_pipeline[i]) &
                (self.survey_kp >= self.route_kp_from[i]) &
                (self.survey_kp <= self.route_kp_to[i]) &
                mask_curve
            )
            self.survey_design_route_curve_radius[cond] = self.route_curve_radius[i]

    def _add_actual_route_curve_radius(self):
        """
        Fit a circle to each group of survey points where the section type is 'Curve' and add
        the fitted radius.

        For each group of survey points (grouped by development, pipeline group, pipeline, survey
        type, and section number) where all points are of type 'Curve' and there are more than 3
        points, fit a circle to the (easting, northing) coordinates and add the resulting radius
        to self.survey_actual_route_curve_radius for those points. Non-curve points or groups with
        insufficient points remain NaN.

        Updates
        -------
        self.survey_actual_route_curve_radius : np.ndarray
            Fitted curve radii for each survey point (NaN for non-curve points or insufficient
            data).

        Returns
        -------
        None
        """
        def calc_radius(x, y, xc, yc):
            return np.sqrt((x - xc) ** 2 + (y - yc) ** 2)
        def fit_circle(x, y):
            x_m = np.mean(x)
            y_m = np.mean(y)
            def f(c):
                radius_i = calc_radius(x, y, *c)
                return radius_i - radius_i.mean()
            center_estimate = x_m, y_m
            center, _ = leastsq(f, center_estimate)
            xc, yc = center
            radius_i = calc_radius(x, y, xc, yc)
            radius = radius_i.mean()
            return radius
        # Group by (development, survey_type, survey_pipeline_group, survey_pipeline, survey_section_no)
        group_tuples = list(zip(
            self.survey_development,
            self.survey_type,
            self.survey_pipeline_group,
            self.survey_pipeline,
            self.survey_section_no
        ))
        unique_groups = set(group_tuples)
        for group in unique_groups:
            mask = (
                (self.survey_development == group[0]) &
                (self.survey_type == group[1]) &
                (self.survey_pipeline_group == group[2]) &
                (self.survey_pipeline == group[3]) &
                (self.survey_section_no == group[4])
            )
            if np.all(self.survey_section_type[mask] == 'Curve') and np.sum(mask) > 3:
                x = self.survey_easting[mask]
                y = self.survey_northing[mask]
                radius = fit_circle(x, y)
                self.survey_actual_route_curve_radius[mask] = radius

    def _transform_pipeline_section_coordinates(self):
        """
        Compute and add section-modified coordinates and KP for each pipeline section.

        For each group of survey points (grouped by development, pipeline group, pipeline,
        survey type, and section number):
        - Shift Easting/Northing so the section starts at (0,0)
        - Rotate the section so it ends at (d, 0) (horizontal line)
        - Compute a section-modified KP (distance along the section, starting at 0)
        The results are stored in self.survey_section_easting_mod,
        self.survey_section_northing_mod, and self.survey_section_kp_mod for each survey point.

        Updates
        -------
        self.survey_section_easting_mod : np.ndarray
            Section-modified easting coordinates for each survey point.
        self.survey_section_northing_mod : np.ndarray
            Section-modified northing coordinates for each survey point.
        self.survey_section_kp_mod : np.ndarray
            Section-modified KP (distance along section, starting at 0) for each survey point.

        Returns
        -------
        None
        """

        group_tuples = list(zip(
            self.survey_development,
            self.survey_type,
            self.survey_pipeline_group,
            self.survey_pipeline,
            self.survey_section_no
        ))
        unique_groups = set(group_tuples)
        for group in unique_groups:
            mask = (
                (self.survey_development == group[0]) &
                (self.survey_type == group[1]) &
                (self.survey_pipeline_group == group[2]) &
                (self.survey_pipeline == group[3]) &
                (self.survey_section_no == group[4])
            )
            idx = np.where(mask)[0]
            if len(idx) == 0:
                continue
            x = self.survey_easting[idx]
            y = self.survey_northing[idx]
            x0, y0 = x[0], y[0]
            x_shift = x - x0
            y_shift = y - y0
            dx = x_shift[-1]
            dy = y_shift[-1]
            theta = -np.arctan2(dy, dx)
            x_mod = x_shift * np.cos(theta) - y_shift * np.sin(theta)
            y_mod = x_shift * np.sin(theta) + y_shift * np.cos(theta)
            kp_mod = np.append(0, np.cumsum(np.diff(self.survey_kp[idx])))
            self.survey_section_easting_mod[idx] = x_mod
            self.survey_section_northing_mod[idx] = y_mod
            self.survey_section_kp_mod[idx] = kp_mod

    def _trim_feature_kps(self):
        """
        Remove survey points where KP is within ±0.2 km of any KP From in the route data for
        matching development, pipeline group, and pipeline.

        Applies a mask to all survey arrays, shortening them in place. This is typically used to
        remove points near mitigation features (e.g., LBMD, PWMD, ILT) from the survey data.

        Updates
        -------
        All survey arrays are filtered in place, reducing their length.

        Returns
        -------
        None
        """
        mitigation_mask = np.isin(self.route_pipeline_section_type, ['LBMD', 'PWMD', 'ILT'])
        keep_mask = np.ones(self.survey_kp.shape[0], dtype=bool)
        for i in np.where(mitigation_mask)[0]:
            cond = (
                (self.survey_development == self.route_development[i]) &
                (self.survey_pipeline_group == self.route_pipeline_group[i]) &
                (self.survey_pipeline == self.route_pipeline[i]) &
                (np.abs(self.survey_kp - self.route_kp_from[i]) <= 0.2)
            )
            keep_mask = keep_mask & ~cond
        # Apply mask to all survey arrays
        self.survey_development = self.survey_development[keep_mask]
        self.survey_type = self.survey_type[keep_mask]
        self.survey_pipeline_group = self.survey_pipeline_group[keep_mask]
        self.survey_pipeline = self.survey_pipeline[keep_mask]
        self.survey_kp = self.survey_kp[keep_mask]
        self.survey_easting = self.survey_easting[keep_mask]
        self.survey_northing = self.survey_northing[keep_mask]
        self.survey_section_type = self.survey_section_type[keep_mask]
        self.survey_section_no = self.survey_section_no[keep_mask]
        self.survey_section_kp_mod = self.survey_section_kp_mod[keep_mask]
        self.survey_section_easting_mod = self.survey_section_easting_mod[keep_mask]
        self.survey_section_northing_mod = self.survey_section_northing_mod[keep_mask]
        self.survey_design_route_curve_radius = self.survey_design_route_curve_radius[keep_mask]
        self.survey_actual_route_curve_radius = self.survey_actual_route_curve_radius[keep_mask]
        self.survey_feature = self.survey_feature[keep_mask]

    def _trim_straight_section_ends(self):
        """
        Trim 50 meters from both ends of all Straight sections, but only when the section changes
        from Curve to Straight or from Straight to Curve.

        Applies a mask to all survey arrays, shortening them in place. Only points at the ends of
        straight sections adjacent to curves are removed.

        Updates
        -------
        All survey arrays are filtered in place, reducing their length.

        Returns
        -------
        None
        """
        n = self.survey_kp.shape[0]
        keep_mask = np.ones(n, dtype=bool)
        # Group by (Development, Pipeline Group, Pipeline, Survey Type, Section No)
        group_tuples = list(zip(
            self.survey_development,
            self.survey_type,
            self.survey_pipeline_group,
            self.survey_pipeline,
            self.survey_section_no
        ))
        unique_groups = set(group_tuples)
        for group in unique_groups:
            mask = (
                (self.survey_development == group[0]) &
                (self.survey_type == group[1]) &
                (self.survey_pipeline_group == group[2]) &
                (self.survey_pipeline == group[3]) &
                (self.survey_section_no == group[4])
            )
            idx = np.where(mask)[0]
            if len(idx) == 0:
                continue
            if not np.all(self.survey_section_type[idx] == 'Straight'):
                continue
            # Find previous and next section types
            prev_idx = idx[0] - 1 if idx[0] > 0 else None
            next_idx = idx[-1] + 1 if idx[-1] < n - 1 else None
            prev_type = self.survey_section_type[prev_idx] if prev_idx is not None else None
            next_type = self.survey_section_type[next_idx] if next_idx is not None else None
            # Only trim if adjacent to a Curve
            if prev_type == 'Curve':
                kp0 = self.survey_kp[idx].min()
                trim_mask = (self.survey_kp[idx] - kp0) < 0.05
                keep_mask[idx[trim_mask]] = False
            if next_type == 'Curve':
                kp1 = self.survey_kp[idx].max()
                trim_mask = (kp1 - self.survey_kp[idx]) < 0.05
                keep_mask[idx[trim_mask]] = False
        # Apply mask to all survey arrays
        self.survey_development = self.survey_development[keep_mask]
        self.survey_type = self.survey_type[keep_mask]
        self.survey_pipeline_group = self.survey_pipeline_group[keep_mask]
        self.survey_pipeline = self.survey_pipeline[keep_mask]
        self.survey_kp = self.survey_kp[keep_mask]
        self.survey_easting = self.survey_easting[keep_mask]
        self.survey_northing = self.survey_northing[keep_mask]
        self.survey_section_type = self.survey_section_type[keep_mask]
        self.survey_section_no = self.survey_section_no[keep_mask]
        self.survey_section_kp_mod = self.survey_section_kp_mod[keep_mask]
        self.survey_section_easting_mod = self.survey_section_easting_mod[keep_mask]
        self.survey_section_northing_mod = self.survey_section_northing_mod[keep_mask]
        self.survey_design_route_curve_radius = self.survey_design_route_curve_radius[keep_mask]
        self.survey_actual_route_curve_radius = self.survey_actual_route_curve_radius[keep_mask]
        self.survey_feature = self.survey_feature[keep_mask]

    def _add_pipeline_group_section(self):
        """
        Adds group-level section type ('Straight' or 'Curve') and section number to each survey
        point.

        For each survey point, adds the group section type (same as section type) and a unique
        group section number within each (development, pipeline group, survey type) group. The
        section number increments for each new continuous section of the same type.

        Updates
        -------
        self.survey_group_section_type : np.ndarray
            Group section type for each survey point.
        self.survey_group_section_no : np.ndarray
            Group section number for each survey point.

        Returns
        -------
        None
        """
        def remove_outliers_iqr(arr, whisker=1.5):
            q1 = np.nanpercentile(arr, 25)
            q3 = np.nanpercentile(arr, 75)
            iqr = q3 - q1
            lower = q1 - whisker * iqr
            upper = q3 + whisker * iqr
            mask = (arr >= lower) & (arr <= upper)
            return arr[mask]
        # Add group section number
        current_section = 0
        group_keys1 = [self.survey_development, self.survey_type, self.survey_pipeline_group]
        group_keys2 = group_keys1 + [self.survey_pipeline, self.survey_section_no]
        prev_keys1 = None
        prev_keys2 = None
        prev_kp = None
        # Group no. loop
        n = self.survey_kp.shape[0]
        group_section_no = np.zeros(n, dtype=int)
        kp_diff = np.diff(self.survey_kp)
        kp_diff_outliers = remove_outliers_iqr(kp_diff)
        avg_kp_diff = np.nanmean(kp_diff_outliers)
        for i in range(n):
            keys1 = tuple(key[i] for key in group_keys1)
            keys2 = tuple(key[i] for key in group_keys2)
            curr_kp = self.survey_kp[i]
            if keys1 != prev_keys1:
                current_section = 1  # Reset to 1 when group_keys changes
            elif keys2 != prev_keys2:
                current_section += 1  # Increase if section type changes
            elif prev_kp is not None and curr_kp - prev_kp > 1.5*avg_kp_diff:
                current_section += 1
            group_section_no[i] = current_section
            prev_keys1 = keys1
            prev_keys2 = keys2
            prev_kp = curr_kp
        self.survey_group_section_no = group_section_no
        self.survey_group_section_type = self.survey_section_type.copy()

    def _transform_pipeline_group_section_coordinates(self):
        """
        Compute and add group section-modified coordinates and KP for each pipeline group
        section.

        For each group of survey points (grouped by development, pipeline group, survey type,
        group section type, and group section number):
        - Shift Easting/Northing so the section starts at (0,0)
        - Rotate the section so it ends at (d, 0) (horizontal line)
        - Compute a group section-modified KP (distance along the section, starting at 0)
        The results are stored in self.survey_group_section_easting_mod,
        self.survey_group_section_northing_mod, and self.survey_group_section_kp_mod for each
        survey point.

        Updates
        -------
        self.survey_group_section_easting_mod : np.ndarray
            Group section-modified easting coordinates for each survey point.
        self.survey_group_section_northing_mod : np.ndarray
            Group section-modified northing coordinates for each survey point.
        self.survey_group_section_kp_mod : np.ndarray
            Group section-modified KP (distance along section, in km) for each survey point.

        Returns
        -------
        None
        """
        n = self.survey_kp.shape[0]
        self.survey_group_section_easting_mod = np.full(n, np.nan, dtype=float)
        self.survey_group_section_northing_mod = np.full(n, np.nan, dtype=float)
        self.survey_group_section_kp_mod = np.full(n, np.nan, dtype=float)
        # Group by (Development, Pipeline Group, Survey Type, Group Section Type)
        group_tuples = list(zip(
            self.survey_development,
            self.survey_type,
            self.survey_pipeline_group,
            self.survey_group_section_type
        ))
        unique_groups = set(group_tuples)
        for group in unique_groups:
            mask = (
                (self.survey_development == group[0]) &
                (self.survey_type == group[1]) &
                (self.survey_pipeline_group == group[2]) &
                (self.survey_group_section_type == group[3])
            )
            idx = np.where(mask)[0]

            # Sort idx by group section no to ensure correct order
            section_nos = self.survey_group_section_no[idx]
            unique_section_nos = np.unique(section_nos)
            shift_x = 0.0
            shift_y = 0.0
            for index, sec_no in enumerate(unique_section_nos):
                sec_mask = idx[section_nos == sec_no]
                x = self.survey_section_easting_mod[sec_mask]
                y = self.survey_section_northing_mod[sec_mask]

                # Compute average slope (angle) for the first 20 and last 20 points
                n_points = len(x)
                n_avg = min(20, n_points // 2)  # Use up to 20, but not more than half the section

                # If not the first section, align to average direction between last N points of
                # previous section and first N of current using robust vector method
                if index == 0:
                    theta = 0.0
                else:
                    # Last n_avg points of previous section
                    x_prev = x_prev_all[-prev_n_avg:]
                    y_prev = y_prev_all[-prev_n_avg:]
                    # First n_avg points of current section
                    x_curr = x[:n_avg]
                    y_curr = y[:n_avg]
                    # Best linear fit for previous section
                    if (
                        len(x_prev) < 2 or
                        np.any(np.isnan(x_prev)) or np.any(np.isnan(y_prev)) or
                        np.any(np.isinf(x_prev)) or np.any(np.isinf(y_prev)) or
                        np.all(x_prev == x_prev[0])
                    ):
                        # Fallback: set coeffs_prev to [0, 0] or skip this section
                        coeffs_prev = [0, 0]
                    else:
                        coeffs_prev = np.polyfit(x_prev, y_prev, 1)
                    slope_prev = coeffs_prev[0]
                    v1 = np.array([1.0, slope_prev])  # direction vector from slope
                    v1_u = v1 / np.linalg.norm(v1)
                    # Best linear fit for current section
                    if (
                        len(x_curr) < 2 or
                        np.any(np.isnan(x_curr)) or np.any(np.isnan(y_curr)) or
                        np.any(np.isinf(x_curr)) or np.any(np.isinf(y_curr)) or
                        np.all(x_curr == x_curr[0])
                    ):
                        coeffs_curr = [0, 0]
                    else:
                        coeffs_curr = np.polyfit(x_curr, y_curr, 1)
                    slope_curr = coeffs_curr[0]
                    v2 = np.array([1.0, slope_curr])
                    v2_u = v2 / np.linalg.norm(v2)
                    # Angle between the two vectors
                    dot = np.dot(v1_u, v2_u)
                    det = v1_u[0]*v2_u[1] - v1_u[1]*v2_u[0]
                    theta = -np.arctan2(det, dot)
                # Previous section
                prev_n_avg = n_avg
                # Shift to origin (0,0)
                x_to_origin = x - x[0]
                y_to_origin = y - y[0]
                # Apply rotation
                x_rot = x_to_origin * np.cos(theta) - y_to_origin * np.sin(theta)
                y_rot = x_to_origin * np.sin(theta) + y_to_origin * np.cos(theta)
                # Save previous
                x_prev_all = x_rot
                y_prev_all = y_rot
                # Apply shift for continuity
                x_mod = x_rot + shift_x
                y_mod = y_rot + shift_y
                # Define variables
                kp_mod = np.insert(np.cumsum(np.diff(self.survey_kp[sec_mask])), 0, 0)
                self.survey_group_section_easting_mod[sec_mask] = x_mod
                self.survey_group_section_northing_mod[sec_mask] = y_mod
                self.survey_group_section_kp_mod[sec_mask] = kp_mod
                # Prepare shift for next section: last point of this section
                shift_x = x_mod[-1]
                shift_y = y_mod[-1]

        # Align all sections to the x-axis
        for group in unique_groups:
            mask = (
                (self.survey_development == group[0]) &
                (self.survey_type == group[1]) &
                (self.survey_pipeline_group == group[2]) &
                (self.survey_group_section_type == group[3])
            )
            idx = np.where(mask)[0]

            # Use the group section modified coordinates
            x = self.survey_group_section_easting_mod[idx]
            y = self.survey_group_section_northing_mod[idx]

            # Compute angle to rotate so last point is on the x-axis
            dx = x[-1]
            dy = y[-1]
            theta = -np.arctan2(dy, dx)

            # Rotate all points
            x_aligned = x * np.cos(theta) - y * np.sin(theta)
            y_aligned = x * np.sin(theta) + y * np.cos(theta)

            # Store the aligned coordinates back
            self.survey_group_section_easting_mod[idx] = x_aligned
            self.survey_group_section_northing_mod[idx] = y_aligned

            # Ensure the max magnitude of northing is positive
            max_north = np.max(self.survey_group_section_northing_mod[idx])
            min_north = np.min(self.survey_group_section_northing_mod[idx])
            if abs(max_north) < abs(min_north):
                # Flip the sign of northing
                self.survey_group_section_northing_mod[idx] = -self.survey_group_section_northing_mod[idx]

class OOSSmoother: # pylint: disable=too-many-arguments, too-many-instance-attributes, too-many-locals
    """
    Class to perform FFT filtering and spectral analysis on 1D signals, grouped by
    (development, survey type, pipeline group, group section type).
    """
    def __init__(
            self,
            *,
            development,
            survey_type,
            pipeline_group,
            group_section_type,
            group_section_number,
            x,
            y,
            fft_cutoff_wl,
            gaussian_bandwidth
        ):
        """
        Initialize an OOSAnonymisation object with route and survey data.

        Parameters
        ----------
        development : array_like
            Development identifier for each point.
        survey_type : array_like
            Survey type for each point.
        pipeline_group : array_like
            Pipeline group for each point.
        group_section_type : array_like
            Group section type for each point.
        group_section_number : array_like
            Group section number for each point.
        x : array_like
            The x-coordinates (e.g., distance or KP) for all points.
        y : array_like
            The y-values (signal) for all points.
        fft_cutoff_wl : float or None, optional
            Wavelength cutoff for FFT filtering. If None, no filtering is applied.
        gaussian_bandwidth : float, optional
            Bandwidth for Gaussian filtering. Default is 4.0.

        Attributes
        ----------
        y_smooth : np.ndarray
            Array of filtered y-values, aligned with input y (NaN for points not in a group).
        freqs : np.ndarray
            Array of frequency values, aligned with input y (NaN for points not in a group).
        fft : np.ndarray
            Array of filtered FFT values, aligned with input y (NaN for points not in a group).
        freqs_raw : np.ndarray
            Array of raw (unfiltered) frequency values, aligned with input y
            (NaN for points not in a group).
        fft_raw : np.ndarray
            Array of raw (unfiltered) FFT values, aligned with input y
            (NaN for points not in a group).
        psd_development : list of np.ndarray
            For each group, an array filled with the development value,
            same length as the PSD frequency array (set by fft_welch).
        psd_survey_type : list of np.ndarray
            For each group, an array filled with the survey type value,
            same length as the PSD frequency array (set by fft_welch).
        psd_survey_number : list of np.ndarray
            For each group, an array filled with the survey number,
            same length as the PSD frequency array (set by fft_welch).
        psd_pipeline_group : list of np.ndarray
            For each group, an array filled with the pipeline group value,
            same length as the PSD frequency array (set by fft_welch).
        psd_group_section_type : list of np.ndarray
            For each group, an array filled with the group section type value,
            same length as the PSD frequency array (set by fft_welch).
        psd_freqs : list of np.ndarray
            List of frequency arrays for each group (set by fft_welch).
        psd_vals : list of np.ndarray
            List of PSD arrays for each group (set by fft_welch).
        y_smooth_gaussian : np.ndarray
            Array of filtered y-values using the gaussian filter,
            aligned with input y (NaN for points not in a group).
        """
        # Convert to arrays
        self.development = np.asarray(development, dtype=object)
        self.survey_type = np.asarray(survey_type, dtype=object)
        self.pipeline_group = np.asarray(pipeline_group, dtype=object)
        self.group_section_type = np.asarray(group_section_type, dtype=object)
        self.group_section_number = np.asarray(group_section_number, dtype=float)
        self.x = np.asarray(x)
        self.y = np.asarray(y)
        # Prepare fft_filter attributes
        self.group_tuples = list(zip(
            self.development,
            self.survey_type,
            self.pipeline_group,
            self.group_section_type,
        ))
        self.unique_groups = sorted(set(self.group_tuples), key=self.group_tuples.index)
        self.fft_cutoff_wl = fft_cutoff_wl
        self.gaussian_bandwidth = gaussian_bandwidth
        # Initialize attributes
        self.y_smooth = np.full_like(self.y, np.nan, dtype=float)
        self.freqs = np.full_like(self.y, np.nan, dtype=float)
        self.fft = np.full_like(self.y, np.nan, dtype=complex)
        self.freqs_raw = np.full_like(self.y, np.nan, dtype=float)
        self.fft_raw = np.full_like(self.y, np.nan, dtype=complex)
        # Prepare fft_welch attributes
        self.psd_development = []
        self.psd_survey_type = []
        self.psd_pipeline_group = []
        self.psd_group_section_type = []
        self.psd_freqs = []
        self.psd_vals = []
        # Prepare gaussian attributes
        self.y_smooth_gaussian = np.full_like(self.y, np.nan, dtype=float)

    def fft_filter(self):
        """
        Apply FFT low-pass filtering to each group, deduplicating (x_g, y_g) pairs within a group
        before filtering.
        The smoothed value is mapped back to all original indices for each unique pair, ensuring
        identical pairs get identical y_smooth values.

        This method also stores the raw (unfiltered) FFT and frequency values for each group in
        the attributes `fft_raw` and `freqs_raw`.

        Sets the following attributes:
        -----------------------------
        y_smooth : ndarray
            Array of filtered y-values, aligned with input y
            (NaN for points not in a group).
        freqs : ndarray
            Array of filtered frequency values, aligned with input y
            (NaN for points not in a group).
        fft : ndarray
            Array of filtered FFT values, aligned with input y
            (NaN for points not in a group).
        freqs_raw : ndarray
            Array of raw (unfiltered) frequency values, aligned with input y
            (NaN for points not in a group).
        fft_raw : ndarray
            Array of raw (unfiltered) FFT values, aligned with input y
            (NaN for points not in a group).

        Returns
        -------
        None
        """
        for group in self.unique_groups:
            mask = (
                (self.development == group[0]) &
                (self.survey_type == group[1]) &
                (self.pipeline_group == group[2]) &
                (self.group_section_type == group[3])
            )
            x_g = self.x[mask]
            y_g = self.y[mask]
            # Deduplicate (x_g, y_g) pairs
            pairs = np.column_stack((x_g, y_g))
            _, unique_idx, inverse_idx = np.unique(pairs, axis=0,
                                                   return_index=True, return_inverse=True)
            x_g_unique = x_g[unique_idx]
            y_g_unique = y_g[unique_idx]
            # FFT filtering on unique pairs
            if len(x_g_unique) < 2:
                # Not enough points to filter
                y_smooth_unique = y_g_unique.copy()
                freqs_g = np.full_like(x_g_unique, np.nan, dtype=float)
                fft_g = np.full_like(x_g_unique, np.nan, dtype=complex)
                fft_vals_g = np.full_like(x_g_unique, np.nan, dtype=complex)
            else:
                dx_g = np.mean(np.diff(x_g_unique))
                if dx_g == 0:
                    fs_g = np.nan
                    continue
                else:
                    fs_g = 1 / dx_g
                fft_vals_g = fft(y_g_unique)
                freqs_g = fftfreq(len(x_g_unique), 1 / fs_g)
                fft_g = np.copy(fft_vals_g)
                if self.fft_cutoff_wl is not None:
                    fft_g[np.abs(freqs_g) > 1 / self.fft_cutoff_wl] = 0
                y_smooth_unique = np.real(ifft(fft_g))
            # Map smoothed values back to all original indices
            y_smooth_g = y_smooth_unique[inverse_idx]
            freqs_g_full = np.full_like(x_g, np.nan, dtype=float)
            fft_g_full = np.full_like(x_g, np.nan, dtype=complex)
            fft_raw_full = np.full_like(x_g, np.nan, dtype=complex)
            freqs_raw_full = np.full_like(x_g, np.nan, dtype=float)
            # For each original index, assign the frequency and fft value from the unique pair
            for i, idx in enumerate(inverse_idx):
                if len(freqs_g) > idx:
                    freqs_g_full[i] = freqs_g[idx]
                    fft_g_full[i] = fft_g[idx]
                    freqs_raw_full[i] = freqs_g[idx]
                    fft_raw_full[i] = fft_vals_g[idx]
            # Assign values
            self.y_smooth[mask] = y_smooth_g
            self.freqs[mask] = freqs_g_full
            self.fft[mask] = fft_g_full
            self.freqs_raw[mask] = freqs_raw_full
            self.fft_raw[mask] = fft_raw_full

    def fft_welch(self, nperseg=256):
        """
        Compute the Power Spectral Density (PSD) using Welch's method for each group.

        This method estimates the distribution of signal power as a function of wavelength.
        By plotting the PSD against wavelength (1/frequency), you can visually identify
        which wavelength bands contain significant noise or signal energy. 
        Typically, noise appears at shorter wavelengths (higher frequencies), while meaningful
        signal features are often found at longer wavelengths. Use this information to select
        an appropriate cutoff wavelength for filtering out noise.

        Sets the following attributes:
        -----------------------------
        psd_development : list of ndarray
            For each group, an array filled with the development value,
            same length as the PSD frequency array.
        psd_survey_type : list of ndarray
            For each group, an array filled with the survey type value,
            same length as the PSD frequency array.
        psd_pipeline_group : list of ndarray
            For each group, an array filled with the pipeline group value,
            same length as the PSD frequency array.
        psd_group_section_type : list of ndarray
            For each group, an array filled with the group section type value,
            same length as the PSD frequency array.
        psd_freqs : list of ndarray
            List of frequency arrays for each group.
        psd_vals : list of ndarray
            List of PSD arrays for each group.

        Returns
        -------
        None
        """
        for group in self.unique_groups:
            mask = (
                (self.development == group[0]) &
                (self.survey_type == group[1]) &
                (self.pipeline_group == group[2]) &
                (self.group_section_type == group[3])
            )
            x_g = self.x[mask]
            y_g = self.y[mask]
            if len(x_g) < 2 or len(y_g) < 2:
                continue
            dx_g = np.mean(np.diff(x_g))
            if dx_g == 0:
                continue
            fs_g = 1 / dx_g
            nperseg_eff = min(nperseg, len(y_g))
            f_welch, pxx_welch = welch(y_g, fs=fs_g, nperseg=nperseg_eff)
            self.psd_development.append(group[0])
            self.psd_survey_type.append(group[1])
            self.psd_pipeline_group.append(group[2])
            self.psd_group_section_type.append(group[3])
            self.psd_freqs.append(f_welch)
            self.psd_vals.append(pxx_welch)

    def gaussian_filter(self):
        """
        Apply Gaussian kernel smoothing to each group, using gaussian_bandwidth.

        The smoothing is performed group-wise, using the same grouping as fft_filter.
        The result is stored in self.y_smooth_gaussian, aligned with input y.

        Sets
        ----
        y_smooth_gaussian : ndarray
            Array of smoothed y-values, aligned with input y (NaN for points not in a group).
        """
        std = 0.37
        b_scaled = self.gaussian_bandwidth / std
        for group in self.unique_groups:
            mask = (
                (self.development == group[0]) &
                (self.survey_type == group[1]) &
                (self.pipeline_group == group[2]) &
                (self.group_section_type == group[3])
            )
            x_g = self.x[mask]
            y_g = self.y[mask]
            y_smooth_g = np.empty_like(y_g, dtype=float)
            for i in range(x_g.size):
                x_left = max(x_g[0], x_g[i] - 2 * b_scaled)
                x_right = min(x_g[i] + 2 * b_scaled, x_g[-1])
                idx = np.where((x_g >= x_left) & (x_g <= x_right))[0]
                xgk = x_g[idx]
                ygk = y_g[idx]
                weight = (
                    1 / ((2 * np.pi) ** 0.5 * std)* np.exp(
                        -0.5 * (np.abs(xgk - x_g[i]) / b_scaled / std) ** 2)
                )
                sumygk = np.dot(weight, ygk)
                sumweight = np.sum(weight)
                if sumweight != 0:
                    y_smooth_g[i] = sumygk / sumweight
                elif ygk.size > 0:
                    y_smooth_g[i] = ygk[0]
                else:
                    y_smooth_g[i] = np.nan  # or 0, or skip, depending on your needs
            self.y_smooth_gaussian[mask] = y_smooth_g
