import Oasys.gRPC


# Metaclass for static properties and constants
class OptionsType(type):
    _props = {'airbag_colour', 'auto_confirm', 'background_colour', 'browse_missing_include_file', 'connection_angle_tol', 'connection_edge_dist', 'connection_file', 'connection_max_thickness', 'connection_model', 'connection_part', 'contacts_colour', 'contour_text_pt_size', 'convert_rbe2_cnrb', 'copy_target_include', 'dyna_version', 'edge_angle', 'edges_ign_pt', 'edit_keep_on_top', 'exception_messages', 'extra_nodes_colour', 'feature_line', 'for_mom_colour', 'graticule_text_size', 'keyout_binary', 'keyout_compress_format', 'keyout_compress_level', 'keyout_compress_switch', 'keyout_i10', 'keyout_large', 'keyout_method', 'keyout_parameter_values', 'keyout_path_type', 'keyout_separator', 'label_colour', 'label_pt_size', 'mass_properties_centre_x', 'mass_properties_centre_y', 'mass_properties_centre_z', 'mass_properties_coordinate_system_type', 'mass_properties_include_attached_mass_deformable_elems', 'mass_properties_include_attached_mass_rigid_elems', 'mass_properties_include_timestep_mass', 'mass_properties_inertia_center', 'mass_properties_local_axes', 'mass_properties_rigid_part_constrained_parts', 'mass_properties_rigid_part_extra_nodes', 'max_widgets', 'max_window_lines', 'merge_rbe_nodes', 'merge_set_collect', 'model_tabs_active', 'node_colour', 'node_replace_asrg', 'nrb_colour', 'overlay_colour', 'overlay_edges', 'pick_window_position', 'property_parameter_names', 'reset_cwd', 'retain_mid_nodes', 'rigid_bodies_colour', 'rot_vels_colour', 'sketch_colour', 'solid_spotweld_diameter', 'spotweld_element_type', 'spotweldbeam_colour_from_panels', 'spr_colour_from_node_sets', 'ssh_buffer_size', 'text_colour', 'timehist_blks_colour', 'title_date_pt_size', 'tracer_partl_colour', 'trans_vels_colour', 'x_sections_colour'}
    _rprops = {'connection_write_flag'}

    def __getattr__(cls, name):
        if name in OptionsType._props:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)
        if name in OptionsType._rprops:
            return Oasys.PRIMER._connection.classGetter(cls.__name__, name)

        raise AttributeError("Options class attribute '{}' does not exist".format(name))


    def __setattr__(cls, name, value):
# If one of the properties we define then set it
        if name in OptionsType._props:
            Oasys.PRIMER._connection.classSetter(cls.__name__, name, value)
            return

# If one of the read only properties we define then error
        if name in OptionsType._rprops:
            raise AttributeError("Cannot set read-only Options class attribute '{}'".format(name))

# Set the property locally
        cls.__dict__[name] = value


class Options(Oasys.gRPC.OasysItem, metaclass=OptionsType):


    def __del__(self):
        if not Oasys.PRIMER._connection:
            return

        if self._handle is None:
            return

        Oasys.PRIMER._connection.destructor(self.__class__.__name__, self._handle)


    def __getattr__(self, name):
# If constructor for an item fails in program, then _handle will not be set and when
# __del__ is called to return the object we will call this to get the (undefined) value
        if name == "_handle":
            return None

        raise AttributeError("Options instance attribute '{}' does not exist".format(name))


    def __setattr__(self, name, value):
# Set the property locally
        self.__dict__[name] = value
