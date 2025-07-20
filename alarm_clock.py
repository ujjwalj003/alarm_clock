import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pygame

# Initialize the PyGame audio mixer with specific settings and load the alarm sound file
pygame.mixer.init(42050, -16, 2, 2048)
alarm_sound = pygame.mixer.Sound("MyAlarm.wav")

# Global flags used to manage the alarm state
start_printed = False
stop_printed = True
done = False
finished = False
stop_clicked = False

class AlarmApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window title and prevent resizing
        self.title("Alarm Clock")
        self.resizable(width=False, height=False)

        # Variables for dropdown selections (Hour, Minute, AM/PM)
        self.hr = tk.IntVar(self)
        self.min = tk.IntVar(self)
        self.ampm = tk.StringVar(self)

        # Default values
        self.hr.set(12)
        self.min.set(0)
        self.ampm.set("AM")

        # Define dropdown options
        hours = list(range(1, 13))
        minutes = ["%02d" % i for i in range(60)]
        ampmlist = ["AM", "PM"]

        # Create dropdowns and pack them
        self.popmenuhours = tk.OptionMenu(self, self.hr, *hours)
        self.popmenuminutes = tk.OptionMenu(self, self.min, *minutes)
        self.popmenuAMPM = tk.OptionMenu(self, self.ampm, *ampmlist)

        self.popmenuhours.pack(side="left")
        tk.Label(text=":").pack(side="left")
        self.popmenuminutes.pack(side="left")
        self.popmenuAMPM.pack(side="left")

        # Buttons for setting, canceling, and stopping the alarm
        self.alarmbutton = tk.Button(self, text="Set Alarm", command=self.start_clock)
        self.cancelbutton = tk.Button(self, text="Cancel Alarm", command=self.stop_clock, state="disabled")
        self.stopalarmbutton = tk.Button(self, text="Stop Alarm", command=self.stop_audio, state="disabled")

        # Pack buttons
        self.alarmbutton.pack()
        self.cancelbutton.pack()
        self.stopalarmbutton.pack()

    def start_clock(self):
        """
        This function initiates the clock loop to check for alarm time.
        """
        global done, start_printed, stop_printed, stop_clicked

        if not done:
            self.cancelbutton.config(state="active")
            self.alarmbutton.config(state="disabled")

            if not start_printed:
                print("Alarm set for {}:{}{}".format(self.hr.get(), "%02d" % self.min.get(), self.ampm.get()))
                start_printed = True
                stop_printed = False

            # Convert 12-hour time to 24-hour format
            if self.ampm.get() == "AM":
                hour_value = self.hr.get() if self.hr.get() != 12 else 0
            elif self.ampm.get() == "PM":
                hour_value = self.hr.get() if self.hr.get() == 12 else self.hr.get() + 12

            # Call alarm checker
            self.Alarm("%02d" % hour_value, "%02d" % self.min.get())

        # Reset state after stopping
        if stop_clicked:
            done = False
            start_printed = False
            stop_clicked = False

    def stop_clock(self):
        """
        Cancels the running alarm before it rings.
        """
        global done, stop_clicked
        print("Alarm set for {}:{}{} has been cancelled".format(self.hr.get(), "%02d" % self.min.get(), self.ampm.get()))
        stop_clicked = True
        done = True
        self.cancelbutton.config(state="disabled")
        self.alarmbutton.config(state="active")

    def stop_audio(self):
        """
        Stops the alarm sound when it's playing.
        """
        pygame.mixer.Sound.stop(alarm_sound)
        self.stopalarmbutton.config(state="disabled")
        self.alarmbutton.config(state="active")

    def Alarm(self, myhour, myminute):
        """
        Checks current time against the alarm time.
        """
        global done, start_printed, finished

        if not done:
            myhour, myminute = str(myhour), str(myminute)

            # Get current system time
            current_time = datetime.now().strftime("%H:%M").split(":")
            hour = current_time[0]
            minute = current_time[1]

            # Check if alarm time matches current time
            if hour == myhour and minute == myminute:
                pygame.mixer.Sound.play(alarm_sound, loops=-1)
                print("Alarm is ringing!")
                done = True
                finished = True
                self.cancelbutton.config(state="disabled")
                self.stopalarmbutton.config(state="active")
            else:
                # Check again after 1 second (recursive loop)
                self.after(1000, self.start_clock)

            done = False

        # Reset flags after alarm has rung
        if finished:
            start_printed = False
            finished = False

# Create and start the app
app = AlarmApp()
app.mainloop()
