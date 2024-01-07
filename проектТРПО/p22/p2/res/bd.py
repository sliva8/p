import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('labb18_bd.db') #установили связь с БД (или создали если ее нет)
        self.c = self.conn.cursor() #создали курсор
        #студенческий отдел кадров
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "student" (
                        "id_student" INTEGER NOT NULL,
                        "FIO" TEXT,
                        "pol" TEXT,
                        "data_rozdenija" TEXT ,
                        "adres" TEXT ,
                        "telefon" TEXT ,
                        "kurs" TEXT ,
                        "god_postuplenija" TEXT ,
                        "god_okonchanija" TEXT ,
                        "nomer_stud_bileta" TEXT ,
                        "id_group" INTEGER,
                        "id_specialnosti" INTEGER,
                        "id_otdelenije" INTEGER,
                        "id_vid_finansirovanija" INTEGER,
                        "id_svedenija_o_roditel" INTEGER,
                         PRIMARY KEY("id_student" AUTOINCREMENT)
                        )''')
        
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "groups" (
                "id_group" INTEGER NOT NULL,
                "N_grupp" TEXT,
                PRIMARY KEY ("id_group" AUTOINCREMENT)
                )'''
        )

        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "specialnosti" (
                "id_specialnosti" INTEGER NOT NULL,
                "Nazvanije_specialnosti" TEXT,
                PRIMARY KEY ("id_specialnosti" AUTOINCREMENT)
                )'''
        )
        
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS "otdelenije" (
                "id_otdelenije" INTEGER NOT NULL,
                "Nazvanije_otdelenije" TEXT,
                PRIMARY KEY ("id_otdelenije" AUTOINCREMENT)
                )'''
        )

        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS  "vid_finansirovanija" (
                "id_vid_finansirovanija" INTEGER NOT NULL,
                "Nazvanije_vid_finansirovanija" TEXT,
                PRIMARY KEY ( "id_vid_finansirovanija" AUTOINCREMENT)
                )'''
        )

        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS  "svedenija_o_roditel" (
                "id_svedenija_o_roditel" INTEGER NOT NULL,
                "FIO_materi" TEXT,
                "FIO_otsa" TEXT,
                "telephon_materi" TEXT,
                "telephon_otsa" TEXT,
                PRIMARY KEY ("id_svedenija_o_roditel" AUTOINCREMENT)
                )'''
        )
        
        self.conn.commit()

db = DB()
