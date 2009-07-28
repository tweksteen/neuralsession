import os
import env
import learn
import process

# TODO : get those names dynamically, see get_managed_apps
MANAGED_APPS = ('itunes', '/Applications/Firefox.app/Contents/MacOS/firefox-bin', 'textmate', 'things')

def get_managed_apps():
    return MANAGED_APPS
    
def main():
    environment = env.get()
    running_apps = process.Process.all()
    names = [ p.command for p in running_apps ]
    for app in get_managed_apps():
        forked = os.fork()
        if not forked: # child
            running = True if app in names else False
            print "Updating NN of", app #   update the neronal network associated
            return

if __name__ == '__main__':
    main()