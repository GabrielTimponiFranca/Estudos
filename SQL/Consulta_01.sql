SELECT 
    CAST(h.E3TimeStamp AS DATE), 
    avg(h.CorrenteA), 
    avg(h.CorrenteB), 
    avg(h.CorrenteC) 
FROM hist_MM_TrafoC h
WHERE h.E3TimeStamp >= SMALLDATETIMEFROMPARTS(2018, 12, 6, 12, 51) 
    AND h.E3TimeStamp <= SMALLDATETIMEFROMPARTS(2018, 12, 08, 12, 51)
GROUP BY CAST(h.E3TimeStamp AS DATE)
ORDER BY CAST(h.E3TimeStamp AS DATE)