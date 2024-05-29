public class Main {
    public static void main(String[] args) {
        MarketDataProcessor processor = new SimpleMarketDataProcessor();
        MarketDataRepository repository = new InMemoryMarketDataRepository();
        MarketDataIngestor ingestor = new InvestingMarketDataIngestor(processor, repository);

        ingestor.ingestData();

        List<MarketData> historicalData = repository.getHistoricalData("USA_10_YR");
        for (MarketData data : historicalData) {
            System.out.println("Date: " + data.getDate() + ", Price: " + data.getPrice());
        }

        // Calculate Bond Price and NPV
        BondPriceCalculator priceCalculator = new SimpleBondPriceCalculator();
        NPVCalculator npvCalculator = new SimpleNPVCalculator();

        double faceValue = 1000; // Example face value
        double couponRate = 0.05; // Example coupon rate (5%)
        int yearsToMaturity = 10; // Example years to maturity
        double marketRate = 0.04; // Example market rate (4%)
        double discountRate = 0.04; // Example discount rate (4%)

        double bondPrice = priceCalculator.calculatePrice(faceValue, couponRate, yearsToMaturity, marketRate);
        double npv = npvCalculator.calculateNPV(faceValue, couponRate, yearsToMaturity, discountRate);

        System.out.println("Bond Price: " + bondPrice);
        System.out.println("NPV: " + npv);
    }
}


public class Main_Lambda {
    public static void main(String[] args) {
        // Existing market data ingestion and processing
        MarketDataProcessor processor = new SimpleMarketDataProcessor();
        MarketDataRepository repository = new InMemoryMarketDataRepository();
        MarketDataIngestor ingestor = new InvestingMarketDataIngestor(processor, repository);

        ingestor.ingestData();

        List<MarketData> historicalData = repository.getHistoricalData("USA_10_YR");
        for (MarketData data : historicalData) {
            System.out.println("Date: " + data.getDate() + ", Price: " + data.getPrice());
        }

        // Bond Price and NPV calculations using lambda expressions
        BondPriceCalculator priceCalculator = (faceValue, couponRate, yearsToMaturity, marketRate) -> {
            double price = 0.0;
            for (int i = 1; i <= yearsToMaturity; i++) {
                price += (faceValue * couponRate) / Math.pow(1 + marketRate, i);
            }
            price += faceValue / Math.pow(1 + marketRate, yearsToMaturity);
            return price;
        };

        NPVCalculator npvCalculator = (faceValue, couponRate, yearsToMaturity, discountRate) -> {
            double npv = 0.0;
            for (int i = 1; i <= yearsToMaturity; i++) {
                npv += (faceValue * couponRate) / Math.pow(1 + discountRate, i);
            }
            npv += faceValue / Math.pow(1 + discountRate, yearsToMaturity);
            return npv;
        };

        double faceValue = 1000; // Example face value
        double couponRate = 0.05; // Example coupon rate (5%)
        int yearsToMaturity = 10; // Example years to maturity
        double marketRate = 0.04; // Example market rate (4%)
        double discountRate = 0.04; // Example discount rate (4%)

        double bondPrice = priceCalculator.calculatePrice(faceValue, couponRate, yearsToMaturity, marketRate);
        double npv = npvCalculator.calculateNPV(faceValue, couponRate, yearsToMaturity, discountRate);

        System.out.println("Bond Price: " + bondPrice);
        System.out.println("NPV: " + npv);
    }
}
  
