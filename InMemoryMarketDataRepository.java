import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class InMemoryMarketDataRepository implements MarketDataRepository {
    private final Map<String, List<MarketData>> dataStore = new HashMap<>();

    @Override
    public void saveData(MarketData marketData) {
        dataStore.putIfAbsent(marketData.getBondSymbol(), new ArrayList<>());
        dataStore.get(marketData.getBondSymbol()).add(marketData);
    }

    @Override
    public List<MarketData> getHistoricalData(String bondSymbol) {
        return dataStore.getOrDefault(bondSymbol, new ArrayList<>());
    }
}
 
