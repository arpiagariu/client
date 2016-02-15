from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default



class TimerCommand(PluginCommand, CloudPluginCommand):

    topics = {"timer": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.timer:
            print("init command timer")
        # try:
        #    value = Default.get_timer()
        # except:
        #    Default.set_timer("off")

    @command
    def do_timer(self, args, arguments):
        """
        ::

            Usage:
                timer on
                timer off
                timer list
                timer start NAME
                timer stop NAME
                timer resume NAME
                timer reset [NAME]

            Description:

                 timer on | off
                     switches timers on and off not yet implemented.
                     If the timer is on each command will be timed and its
                     time is printed after the command. Please note that
                     background command times are not added.

                timer list
                    list all timers

                timer start NAME
                    starts the timer with the name. A start resets the timer to 0.

                timer stop NAME
                    stops the timer

                timer resume NAME
                    resumes the timer

                timer reset NAME
                    resets the named timer to 0. If no name is specified all
                    timers are reset

        """
        # print arguments
        # print "args", args


        if arguments["on"]:
            Default.set_timer("on")
            Console.ok("Switch timer on")
        elif arguments["off"]:
            Default.set_timer("off")
            Console.ok("Switch timer off")
        elif arguments["list"]:
            # timer = Default.timer()
            Console.ok("Timer is switched {}".format(timer))
        elif arguments["start"]:
            # Default.set_timer("off")
            name = arguments("NAME")
            Console.ok("Start timer")
        elif arguments["stop"]:
            # Default.set_timer("off")
            name = arguments("NAME")
            Console.ok("Stop timer")
        elif arguments["reset"]:
            # Default.set_timer("off")
            name = arguments("NAME")
            Console.ok("Stop timer")



