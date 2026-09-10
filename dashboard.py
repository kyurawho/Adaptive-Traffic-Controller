import cv2
import numpy as np
from config import *
from region_counter import trafficController, statusLampu


class Dashboard:

    def __init__(self):
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT


    def draw(self, frames, counts, lights, remaining, phase, current, green_times):

        dashboard = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # =================================================
        # VIDEO
        # =================================================
        for i in range (len(frames)) :
            x = i % 2
            y = i // 2
            # frame = cv2.resize(

            #     frames[i],
            #     (VIDEO_WIDTH, VIDEO_HEIGHT)

            # )


            # row = i // 2

            # col = i % 2


            # x = col * VIDEO_WIDTH

            # y = row * VIDEO_HEIGHT


            # dashboard[

            #     y:y + VIDEO_HEIGHT,

            #     x:x + VIDEO_WIDTH

            # ] = frame
            y_videoheight = (y*VIDEO_HEIGHT)
            x_videowidth = (x*VIDEO_WIDTH)
            #print(f"y = {y_videoheight} ; x = {x_videowidth}")
            frame = cv2.resize(
                frames[(y*2)+x],
                (VIDEO_WIDTH, VIDEO_HEIGHT)
            )
            dashboard[y_videoheight:(y_videoheight + VIDEO_HEIGHT), x_videowidth:(x_videowidth + VIDEO_WIDTH)] = frame


        # =================================================
        # PANEL
        # =================================================

        x = VIDEO_WIDTH * 2 + 20


        cv2.putText(

            dashboard,

            TITLE,

            (x, 40),

            FONT,

            0.7,

            WHITE,

            2

        )


        y = 100


        for i in range(4):

            # Warna lampu

            if lights[i] == "GREEN":

                color = GREEN

            elif lights[i] == "YELLOW":

                color = YELLOW

            else:

                color = RED


            # Lampu

            cv2.circle(

                dashboard,

                (x + 20, y),

                15,

                color,

                -1

            )


            # Status

            cv2.putText(

                dashboard,

                f"S{i+1}",

                (x + 50, y),

                FONT,

                0.6,

                WHITE,

                2

            )


            cv2.putText(

                dashboard,

                f"Queue : {counts[i]}",

                (x + 50, y + 25),

                FONT,

                0.5,

                WHITE,

                1

            )


            cv2.putText(

                dashboard,

                f"Green : {green_times[i]}s",

                (x + 200, y + 25),

                FONT,

                0.5,

                WHITE,

                1

            )


            y += 65


        # =================================================
        # CURRENT
        # =================================================

        cv2.putText(

            dashboard,

            f"Current : S{current + 1}",

            (x, 390),

            FONT,

            0.8,

            GREEN,

            2

        )


        cv2.putText(

            dashboard,

            f"Phase : {phase}",

            (x, 430),

            FONT,

            0.8,

            YELLOW,

            2

        )


        cv2.putText(

            dashboard,

            f"Countdown : {remaining}s",

            (x, 470),

            FONT,

            0.8,

            WHITE,

            2

        )


        return dashboard
    
    def drawDashboard(self, frames, controller : trafficController):
        dashboard = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # ======================VIDEO===========================
        for i in range (len(frames)) :
            x = i % 2
            y = i // 2

            y_videoheight = (y*VIDEO_HEIGHT)
            x_videowidth = (x*VIDEO_WIDTH)
            #print(f"y = {y_videoheight} ; x = {x_videowidth}")
            frame = cv2.resize(
                frames[(y*2)+x],
                (VIDEO_WIDTH, VIDEO_HEIGHT)
            )
            dashboard[y_videoheight:(y_videoheight + VIDEO_HEIGHT), x_videowidth:(x_videowidth + VIDEO_WIDTH)] = frame

        # =======================PANEL==========================
        x = VIDEO_WIDTH * 2 + 20
        cv2.putText(dashboard, TITLE, (x, 40), FONT, 0.7, WHITE, 2, )
        #y = 100
        for i in range(0, 4):
            # Warna lampu
            lampu = controller.getLampu(i)
            color = BLACK
            if lampu.status == statusLampu.RED :
                color = RED
            elif lampu.status == statusLampu.YELLOW :
                color = YELLOW
            elif lampu.status == statusLampu.GREEN:
                color = GREEN
            y = 100 + (50 * i)
            cv2.circle(dashboard, (x + 20, y), 15, color, -1)
            cv2.putText(dashboard, f"{lampu.nama}", (x + 50, y), FONT, 0.6, WHITE, 2)
            cv2.putText(dashboard, f"Queue : {lampu.jmlQueue}", (x + 50, y + 25), FONT, 0.5, WHITE, 1)
            cv2.putText(dashboard, f"Green : {controller.getProbabilitasGreenTime(i)}s", (x + 200, y + 25), FONT, 0.5, WHITE, 1)
            #cv2.putText(dashboard, f"Current : S{current + 1}", (x, 390), FONT, 0.8, GREEN, 2)
            #cv2.putText(dashboard, f"Phase : {phase}", (x, 430), FONT, 0.8, YELLOW, 2)
            #cv2.putText(dashboard, f"Countdown : {remaining}s", (x, 470), FONT, 0.8, WHITE, 2)

        return dashboard