USE PortfolioProject_MarketingAnalytics;

SELECT 
	ReviewID,
	CustomerID,
	ProductID,
	ReviewDate,
	Rating,
	REPLACE(ReviewText,'  ',' ') AS ReviewText
FROM 
	dbo.customer_reviews