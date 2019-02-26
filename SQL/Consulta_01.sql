SELECT 
    CAST(h.E3TimeStamp AS DATE), 
    avg(h.CorrenteA), 
    avg(h.CorrenteB), 
    avg(h.CorrenteC),
    avg(h.Consumo)  
FROM hist_TrafoC h
GROUP BY CAST(h.E3TimeStamp AS DATE)
ORDER BY CAST(h.E3TimeStamp AS DATE)

SELECT  
    CONVERT(SMALLDATETIME, CONCAT(
    CAST(tA.E3TimeStamp AS date), ' ',   
    DATEPART(HOUR,tA.E3TimeStamp), ':00')) AS Data,
    ISNULL(FORMAT(max(tA.Consumo) - LAG(max(tA.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC), 'N', 'de-de'), 0) AS TrafoA,
    ISNULL(FORMAT(max(tB.Consumo) - LAG(max(tB.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC), 'N', 'de-de'), 0) AS TrafoB,
    ISNULL(FORMAT(max(tC.Consumo) - LAG(max(tC.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC), 'N', 'de-de'), 0) AS TrafoC,
    ISNULL(FORMAT(max(tA.Consumo) - LAG(max(tA.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC)+ 
    max(tB.Consumo) - LAG(max(tB.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC)+
    max(tC.Consumo) - LAG(max(tC.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC), 'N', 'de-de'), 0) AS Total
FROM GrandeRio.dbo.hist_TrafoA tA
INNER JOIN GrandeRio.dbo.hist_TrafoB tB ON tB.E3TimeStamp = tA.E3TimeStamp 
INNER JOIN GrandeRio.dbo.hist_TrafoC tC ON tC.E3TimeStamp = tA.E3TimeStamp 
WHERE CAST(tA.E3TimeStamp AS date) BETWEEN (DATEADD(DAY, -8, GETDATE())) AND DATEADD(DAY, 0, GETDATE())
GROUP BY CAST(tA.E3TimeStamp AS date), DATEPART(HOUR,tA.E3TimeStamp)
ORDER BY Data ASC

SELECT  
    CONVERT(SMALLDATETIME, CONCAT(
    CAST(tA.E3TimeStamp AS date), ' ',   
    DATEPART(HOUR,tA.E3TimeStamp), ':00')) AS Data,
    ISNULL(FORMAT(max(tA.Consumo) - LAG(max(tA.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC), 'N', 'de-de'), 0) AS TrafoC
FROM GrandeRio.dbo.hist_TrafoA tA
WHERE CAST(tA.E3TimeStamp AS date) BETWEEN (DATEADD(DAY, -8, GETDATE())) AND DATEADD(DAY, 0, GETDATE())
GROUP BY CAST(tA.E3TimeStamp AS date), DATEPART(HOUR,tA.E3TimeStamp)
ORDER BY Data ASC