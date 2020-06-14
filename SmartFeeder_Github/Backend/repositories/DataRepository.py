from .Database import Database

class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_water():
        sql = "SELECT Waarde FROM smartfeederdb.metingen WHERE MetingID = (SELECT MAX(MetingID) FROM smartfeederdb.metingen WHERE SensorID = 1);"
        return Database.get_rows(sql)

    @staticmethod
    def read_IR():
        sql = "SELECT * FROM (SELECT * FROM smartfeederdb.metingen WHERE ActieCode = 'VOEDING' ORDER BY MetingID DESC LIMIT 2) sub ORDER BY MetingID ASC;"
        return Database.get_rows(sql)

    @staticmethod
    def read_portie():
        sql = "SELECT * FROM (SELECT * FROM smartfeederdb.metingen WHERE ActieCode = 'PORTIE' ORDER BY MetingID DESC LIMIT 1) sub ORDER BY MetingID ASC;"
        return Database.get_rows(sql)

    @staticmethod
    def read_porties():
        sql = "SELECT Waarde, Datum FROM smartfeederdb.metingen WHERE ActieCode = 'PORTIE' ORDER BY MetingID ASC LIMIT 14;"
        return Database.get_rows(sql)

    @staticmethod
    def read_voedermomenten():
        sql = "SELECT VoedermomentID,Uur, Gewicht FROM voedermomenten;"
        return Database.get_rows(sql)

    @staticmethod
    def read_voedermoment(voedermomentid):
        sql = "SELECT * FROM smartfeederdb.voedermomenten WHERE VoedermomentID = %s;"
        params = [voedermomentid]
        return Database.get_one_row(sql, params)


    # ##########################################      DELETE     ####################################################
    @staticmethod
    def delete_voedermoment(voedermomentid):
        sql = "DELETE from smartfeederdb.voedermomenten WHERE voedermomentID = %s"
        params = [voedermomentid]
        return Database.execute_sql(sql, params)


    ###########################################       CREATE      ####################################################
    @staticmethod
    def create_voedermoment(FeederCode, Uur, Gewicht):
        sql = "INSERT INTO smartfeederdb.voedermomenten (FeederCode, Uur, Gewicht) VALUES (%s,%s,%s);"
        params = [FeederCode, Uur, Gewicht]
        return Database.execute_sql(sql, params)

    def create_meting(SensorID,ActieCode,FeederCode, Uur, Gewicht):
        sql= "INSERT INTO metingen (SensorID, ActieCode,FeederCode,Waarde,Datum) Values (%s,%s,%s,%s,%s)"
        params = [SensorID,ActieCode,FeederCode, Uur, Gewicht]
        return Database.execute_sql(sql, params)
