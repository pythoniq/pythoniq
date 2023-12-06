from bootstrap.app import app

"""
# --------------------------------------------------------------------------
# Register The Auto Loader
# --------------------------------------------------------------------------
#
# Composer provides a convenient, automatically generated class loader
# for our application. We just need to utilize it! We'll require it
# into the script here so that we do not have to worry about the
# loading of any of our classes manually. It's great to relax.
#
"""

kernel = app.make('kernel', [1])

status = kernel.handle()

"""
# --------------------------------------------------------------------------
# Run The Adonis Application
# --------------------------------------------------------------------------
#
# When we run the console application, the current CLI command will be
# executed in this console and the response sent back to a terminal
# or another output device for the developers. Here goes nothing!
#
"""
"""
kernel.terminate(input, status)

exit(status)
"""
