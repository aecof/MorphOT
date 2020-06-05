# vim: set expandtab shiftwidth=4 softtabstop=4:

from chimerax.core.toolshed import BundleAPI
from chimerax.core.commands import FloatArg, FloatsArg, CmdDesc, register, BoolArg, StringArg, EnumOf, IntArg, Int3Arg, ModelIdArg
from chimerax.map import MapsArg, MapStepArg, Float1or3Arg, ValueTypeArg
from chimerax.map.mapargs import Float2Arg, MapRegionArg
# Subclass from chimerax.core.toolshed.BundleAPI and
# override the method for registering commands,
# inheriting all other methods from the base class.
class _MyAPI(BundleAPI):

    api_version = 1     # register_command called with BundleInfo and
                        # CommandInfo instance instead of command name
                        # (when api_version==0)
    
    # Override method
    @staticmethod
    def register_command(bi, ci, logger):
        # bi is an instance of chimerax.core.toolshed.BundleInfo
        # ci is an instance of chimerax.core.toolshed.CommandInfo
        # logger is an instance of chimerax.core.logger.Logger

        # This method is called once for each command listed
        # in bundle_info.xml.  Since we list two commands,
        # we expect two calls to this method.

        # We check the name of the command, which should match
        # one of the ones listed in bundle_info.xml
        # (without the leading and trailing whitespace),
        # and import the function to call and its argument
        # description from the ``cmd`` module.
        # If the description does not contain a synopsis, we
        # add the one in ``ci``, which comes from bundle_info.xml.
        # We then register the function as the command callback
        # with the chimerax.core.commands module.
        from chimerax.core.commands import register
        if ci.name == 'volumeperso morphOT':
            from . import morph
            from . import cmd
            func = cmd.volume_morphOT
            varg = cmd.varg
            ssm_kw = cmd.ssm_kw
            morphot_desc = CmdDesc(required = varg,
                            keyword = [('frames', IntArg),
                                        ('start', FloatArg),
                                        ('play_step', FloatArg),
                                        ('play_direction', IntArg),
                                        ('play_range', Float2Arg),
                                        ('add_mode', BoolArg),
                                        ('constant_volume', BoolArg),
                                        ('scale_factors', FloatsArg),
                                        ('hide_original_maps', BoolArg),
                                        ('interpolate_colors', BoolArg)] + ssm_kw,
                            synopsis = 'OT interpolate maps')
            register(ci.name, morphot_desc, func)

        if ci.name == 'volumeperso onebarycenter' : 
            from . import morph
            from . import cmd 
            func = cmd.volume_barycenterOT
            varg = cmd.varg 
            ssm_kw = cmd.ssm_kw 
            onebarycenter_desc = CmdDesc(required = varg + [('weights', Float2Arg)],
                                keyword = [
                                            ('niter', IntArg),
                                            ('reg', FloatArg),
                                            ('interpolate_colors', BoolArg)] + ssm_kw,
                                synopsis = 'OT barycenter maps')
            register(ci.name, onebarycenter_desc, func)

        
    
# Create the ``bundle_api`` object that ChimeraX expects.
bundle_api = _MyAPI()
