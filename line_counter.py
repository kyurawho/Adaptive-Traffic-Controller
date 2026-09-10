class LineCounter:

    def __init__(self, line):

        self.line = line

        # Menyimpan posisi terakhir
        # setiap ID kendaraan

        self.previous_positions = {}

        # ID kendaraan yang sudah pernah
        # crossing line

        self.counted_ids = set()


    # =====================================================
    # CEK SISI KENDARAAN TERHADAP GARIS
    # =====================================================

    def get_side(self, point):

        x, y = point

        (x1, y1), (x2, y2) = self.line


        value = (

            (x2 - x1) * (y - y1)

            -

            (y2 - y1) * (x - x1)

        )


        if value > 0:

            return 1


        elif value < 0:

            return -1


        else:

            return 0


    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, detections):

        entered_ids = []


        for detection in detections:

            track_id = detection["id"]

            current_position = detection["center"]


            # =============================================
            # Posisi sebelumnya
            # =============================================

            previous_position = (

                self.previous_positions.get(

                    track_id

                )

            )


            # =============================================
            # Kalau belum pernah terlihat
            # =============================================

            if previous_position is None:

                self.previous_positions[

                    track_id

                ] = current_position

                continue


            # =============================================
            # Sisi sebelumnya
            # =============================================

            previous_side = self.get_side(

                previous_position

            )


            # =============================================
            # Sisi sekarang
            # =============================================

            current_side = self.get_side(

                current_position

            )


            # =============================================
            # CEK CROSSING
            # =============================================

            crossed = (

                previous_side != 0

                and

                current_side != 0

                and

                previous_side != current_side

            )


            # =============================================
            # KALAU CROSSING
            # =============================================

            if crossed:

                if track_id not in self.counted_ids:

                    entered_ids.append(

                        track_id

                    )

                    self.counted_ids.add(

                        track_id

                    )


            # =============================================
            # UPDATE POSISI
            # =============================================

            self.previous_positions[

                track_id

            ] = current_position


        return entered_ids


    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        self.counted_ids.clear()