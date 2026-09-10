import time

from config import (
    GREEN_PER_VEHICLE,
    MIN_GREEN,
    MAX_GREEN,
    YELLOW_TIME,
    ALL_RED_TIME
)


class TrafficController:

    def __init__(self):

        # =================================================
        # SIMPANG AKTIF
        # =================================================

        self.current = 0


        # =================================================
        # STATUS LAMPU
        # =================================================

        self.lights = [

            "GREEN",

            "RED",

            "RED",

            "RED"

        ]


        # =================================================
        # JUMLAH ANTRIAN
        # =================================================

        self.vehicle_count = [

            0,

            0,

            0,

            0

        ]


        # =================================================
        # GREEN TIME
        # =================================================

        self.green_time = [

            MIN_GREEN,

            MIN_GREEN,

            MIN_GREEN,

            MIN_GREEN

        ]


        # =================================================
        # TIMER
        # =================================================

        self.remaining = MIN_GREEN


        # =================================================
        # PHASE
        # =================================================

        self.phase = "GREEN"


        # =================================================
        # REAL TIME
        # =================================================

        self.last_update = time.time()


    # =====================================================
    # HITUNG GREEN TIME
    # =====================================================

    def calculate_green(self, queue):

        green = (

            MIN_GREEN

            +

            queue * GREEN_PER_VEHICLE

        )


        green = min(

            green,

            MAX_GREEN

        )


        return green


    # =====================================================
    # KENDARAAN MASUK SAAT MERAH
    # =====================================================

    def vehicle_entered(self, intersection):

        # Hanya dihitung kalau lampu MERAH

        if (

            intersection != self.current

            or

            self.phase != "GREEN"

        ):

            self.vehicle_count[

                intersection

            ] += 1


    # =====================================================
    # RESET QUEUE
    # =====================================================

    def reset_queue(self, intersection):

        self.vehicle_count[

            intersection

        ] = 0


    # =====================================================
    # UPDATE
    # =====================================================

    def update(self):

        now = time.time()


        # Timer hanya update tiap 1 detik

        if now - self.last_update < 1:

            return


        self.last_update = now


        self.remaining -= 1


        # =================================================
        # GREEN
        # =================================================

        if self.phase == "GREEN":

            if self.remaining <= 0:

                self.phase = "YELLOW"


                self.lights[

                    self.current

                ] = "YELLOW"


                self.remaining = YELLOW_TIME


        # =================================================
        # YELLOW
        # =================================================

        elif self.phase == "YELLOW":

            if self.remaining <= 0:

                self.phase = "ALL_RED"


                self.lights[

                    self.current

                ] = "RED"


                self.remaining = ALL_RED_TIME


        # =================================================
        # ALL RED
        # =================================================

        elif self.phase == "ALL_RED":

            if self.remaining <= 0:

                # =========================================
                # PINDAH SIMPANG
                # =========================================

                self.current = (

                    self.current + 1

                ) % 4


                # =========================================
                # RESET QUEUE SIMPANG BARU
                # =========================================

                self.reset_queue(

                    self.current

                )


                # =========================================
                # HITUNG GREEN TIME
                # =========================================

                queue = self.vehicle_count[

                    self.current

                ]


                self.green_time[

                    self.current

                ] = self.calculate_green(

                    queue

                )


                # =========================================
                # SET SEMUA MERAH
                # =========================================

                self.lights = [

                    "RED",

                    "RED",

                    "RED",

                    "RED"

                ]


                # =========================================
                # SIMPANG BARU HIJAU
                # =========================================

                self.lights[

                    self.current

                ] = "GREEN"


                self.phase = "GREEN"


                self.remaining = (

                    self.green_time[

                        self.current

                    ]

                )


    # =====================================================
    # GETTER
    # =====================================================

    def get_lights(self):

        return self.lights


    def get_remaining(self):

        return self.remaining


    def get_counts(self):

        return self.vehicle_count


    def get_current(self):

        return self.current


    def get_green_time(self):

        return self.green_time


    def get_phase(self):

        return self.phase