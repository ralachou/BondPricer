public interface BondPriceCalculator {
    double calculatePrice(double faceValue, double couponRate, int yearsToMaturity, double marketRate);
}

public interface NPVCalculator {
    double calculateNPV(double faceValue, double couponRate, int yearsToMaturity, double discountRate);
}
