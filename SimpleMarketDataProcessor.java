import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class SimpleMarketDataProcessor implements MarketDataProcessor {
    @Override
    public MarketData processRawData(String rawData) {
        // Simplified example, real implementation would parse the actual HTML content
        // Assume rawData contains date and price in a simple format
        String[] data = rawData.split(",");
        String bondSymbol = "USA_10_YR";
        LocalDate date = LocalDate.parse(data[0], DateTimeFormatter.ofPattern("yyyy-MM-dd"));
        double price = Double.parseDouble(data[1]);

        return new MarketData(bondSymbol, date, price);
    }
}
