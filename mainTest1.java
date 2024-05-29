import java.util.List;

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
    }
}
