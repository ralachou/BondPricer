public class SimpleNPVCalculator implements NPVCalculator {
    @Override
    public double calculateNPV(double faceValue, double couponRate, int yearsToMaturity, double discountRate) {
        double npv = 0.0;
        for (int i = 1; i <= yearsToMaturity; i++) {
            npv += (faceValue * couponRate) / Math.pow(1 + discountRate, i);
        }
        npv += faceValue / Math.pow(1 + discountRate, yearsToMaturity);
        return npv;
    }
}
