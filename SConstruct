import saliweb.build

vars = Variables('config.py')
env = saliweb.build.Environment(vars, ['conf/live.conf'], service_module='mist')
Help(vars.GenerateHelpText(env))

env.InstallAdminTools()

Export('env')
SConscript('backend/mist/SConscript')
SConscript('frontend/mist/SConscript')
SConscript('test/SConscript')
