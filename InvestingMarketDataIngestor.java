import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class InvestingMarketDataIngestor implements MarketDataIngestor {
    private final MarketDataProcessor processor;
    private final MarketDataRepository repository;

    public InvestingMarketDataIngestor(MarketDataProcessor processor, MarketDataRepository repository) {
        this.processor = processor;
        this.repository = repository;
    }

    @Override
    public void ingestData() {
        try {
            URL url = new URL("https://www.investing.com/bonds/usa-10-yr-bond-yield-historical-data");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");

            Scanner sc = new Scanner(url.openStream());
            StringBuilder rawData = new StringBuilder();
            while (sc.hasNext()) {
                rawData.append(sc.nextLine());
            }
            sc.close();

            MarketData marketData = processor.processRawData(rawData.toString());
            repository.saveData(marketData);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
