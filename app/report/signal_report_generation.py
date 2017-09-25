from app import db1
from datetime import datetime
from sqlalchemy import text


# Signal strength mean by antenna
def signal_strength_mean_for_antenna(min_date=datetime(2015, 1, 1),
                                     max_date=None):
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT
      c2.carrier_id, c2.antenna_id,
      c2.size AS observations,
      CASE WHEN c2.size = 0 THEN 0
           ELSE 10 * (ln(c2.ponderation / c2.size) / ln(10))
           END AS signal_mean
    FROM
    (SELECT
      c1.carrier_id, c1.antenna_id,
      sum(c1.size) as size,
      sum(c1.ponderation) as ponderation
    FROM
    (SELECT
      sims.carrier_id,
      antennas.id as antenna_id,
      gsm_events.signal_strength_size as size,
      gsm_events.signal_strength_size * power(10,(gsm_events.signal_strength_mean)/10.0) as ponderation
    FROM
      public.antennas,
      public.gsm_events,
      public.sims
    WHERE
      gsm_events.antenna_id = antennas.id AND
      gsm_events.sim_serial_number = sims.serial_number AND
      gsm_events.date BETWEEN :min_date AND :max_date
    ) AS c1
    GROUP BY carrier_id, antenna_id) AS c2;""")

    result = db1.session.query().with_labels().add_columns("carrier_id", "antenna_id", "observations",
                                                           "signal_mean").from_statement(
        stmt).params(
        min_date=min_date, max_date=max_date)

    final = [dict(carrier_id=row[0], antenna_id=row[1], observations=row[2], signal_mean=row[3]) for row in
             result.all()]

    return final
