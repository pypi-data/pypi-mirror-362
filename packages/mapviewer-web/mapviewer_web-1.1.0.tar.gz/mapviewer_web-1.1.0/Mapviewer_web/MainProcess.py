from Mapviewer_web.utils.app_notable import app
import optparse
def start_app(args=None):
    parser = optparse.OptionParser(usage="%Mapviewer-web [options] arg")
    parser.add_option("--port",      dest="Port", type="string", \
            help="State the port of the web app.")
    parser.add_option("--mode", dest="Mode", type="string", \
            help="Select if the app is ran locally or remotely")
    (CommandOptions, args) = parser.parse_args()

    if CommandOptions.Mode == 'local':
        host = "127.0.0.1"
    elif CommandOptions.Mode == 'remote':
        host = "0.0.0.0"
    else:
        host = "127.0.0.1"

    if CommandOptions.Port == None:
        port = 9928
    else:
        port = int(CommandOptions.Port)

    app.run_server(debug=False, host=host, port=port)
