public interface MarketDataIngestor {
    void ingestData();
}

public interface MarketDataProcessor {
    MarketData processRawData(String rawData);
}

public interface MarketDataRepository {
    void saveData(MarketData marketData);
    List<MarketData> getHistoricalData(String bondSymbol);
}

public class MarketData {
    private String bondSymbol;
    private LocalDate date;
    private double price;

    // Constructors, getters, and setters
}
