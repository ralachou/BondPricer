public class SimpleBondPriceCalculator implements BondPriceCalculator {
    @Override
    public double calculatePrice(double faceValue, double couponRate, int yearsToMaturity, double marketRate) {
        double price = 0.0;
        for (int i = 1; i <= yearsToMaturity; i++) {
            price += (faceValue * couponRate) / Math.pow(1 + marketRate, i);
        }
        price += faceValue / Math.pow(1 + marketRate, yearsToMaturity);
        return price;
    }
}
