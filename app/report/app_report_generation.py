from app import db1
from datetime import datetime
from sqlalchemy import text


def app_report(min_date=datetime(2015, 1, 1), max_date=None):
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    from app.models_server.carrier import Carrier
    carriers_id = [c.id for c in Carrier.query.all()]
    carriers_id.append("ALL_CARRIERS")
    network_type = {"MOBILE": 1, "WIFI": 6}
    connection_mode = {"UPLOAD": "tx_bytes", "DOWNLOAD": "rx_bytes", "ALL": ""}
    final = {}

    # carrier analysis
    for carrier in carriers_id:
        final[carrier] = {}

        if carrier == "ALL_CARRIERS":
            carrier_stmt = ""
        else:
            carrier_stmt = "sims.serial_number = application_traffic_events.sim_serial_number AND" \
                           " sims.carrier_id = :carrier_id AND"

        for type, value in network_type.items():
            final[carrier][type] = {}
            for mode, name in connection_mode.items():
                final[carrier][type][mode] = {}

                if mode == "ALL":
                    connection_stmt = "SUM(application_traffic_events.tx_bytes + " +\
                                      "application_traffic_events.rx_bytes) AS bytes,"
                else:
                    connection_stmt = "SUM(application_traffic_events." + name + ") AS bytes,"

                stmt = text(
                    """
                     SELECT
                        QUERY.bytes / NULLIF(QUERY.devices,0) as bytes_per_user,
                        QUERY.bytes,
                        QUERY.devices,
                        QUERY.app_name
                     FROM
                        (SELECT
                            """ + connection_stmt + """
                            applications.package_name as app_name,
                            COUNT (DISTINCT devices.device_id) as devices
                        FROM
                            public.applications,
                            public.application_traffic_events,
                            public.devices,
                            public.sims
                        WHERE
                            application_traffic_events.device_id = devices.device_id AND
                             """ + carrier_stmt + """
                            application_traffic_events.application_id = applications.id AND
                            application_traffic_events.network_type = :network_type AND
                            application_traffic_events.date BETWEEN :min_date AND :max_date
                        GROUP BY applications.package_name
                        ORDER BY bytes DESC) AS QUERY
                     ORDER BY bytes_per_user DESC LIMIT :number_app;""")

                result = db1.session.query().add_columns("bytes_per_user", "bytes", "devices",
                                                         "app_name").from_statement(stmt).params(
                    min_date=min_date, max_date=max_date, network_type=value, carrier_id=carrier, number_app=10)
                count = 1
                for row in result.all():
                    final[carrier][type][mode][count] = dict(bytes_per_user=str(row[0]), total_bytes=str(row[1]),
                                                             total_devices=row[2],
                                                             app_name=str(row[3]))
                    count = count + 1

    return final
