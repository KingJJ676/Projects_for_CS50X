# Credit Card Discriminator
This is a discriminator that checks if a given credit card number is valid, and if valid, which of the companies mentioned below it is from.  

## Credit Cards
- **American Express:**
  - 15 digits
  - starts with 34 or 37
- **MasterCard:**
  - 16 digits
  - starts with 51,52,53,54 or 55
- **Visa:**
  - 13 or 16 digits
  - starts with 4
 
## Luhn's Algorithm
Use Luhn's Algorithm to check if the card number is valid.  

**Luhn's Algorithm:**
1. Multiply every other digit by 2, starting with the number’s second-to-last digit, and then add those products’ digits together.  
2. Add the sum to the sum of the digits that weren’t multiplied by 2.  
3. If the total’s last digit is 0 (or, put more formally, if the total modulo 10 is congruent to 0), the number is valid!
