USE PortfolioProject_MarketingAnalytics;
SELECT ProductID,ProductName,Price,
CASE
	WHEN Price<50 THEN 'Low'
	WHEN Price BETWEEN 50 AND 200 THEN 'Medium'
	ELSE 'High'
END AS PriceCategory

FROM dbo.products;
