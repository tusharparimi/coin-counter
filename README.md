# coin-counter
The coin-counter app detected coins on a table and extracts SIFT features to detect the denomination of the coin and the values are added to count the total value on the table.

### Results
Yes, I used a toilet paper roll for the camera stand... lol :toilet:

<img width="146" alt="image" src="https://github.com/tusharparimi/coin-counter/assets/93556280/3506f50f-17e9-4909-9bbb-ac1eb887fa3c">
<img width="148" alt="image" src="https://github.com/tusharparimi/coin-counter/assets/93556280/bbc6e079-7453-4c76-a79e-32cc7cb53535">

video- https://youtu.be/7mIdzkl1AlA?si=CK29AWPYaMBB3nIa

### Implementation notes
- Used indian coins.
- Only detects 5 and 10 rupees coins (2 denominations)
- Good stable results with both coins individually or together in the same frame.
- Fixed the camera position very close to the coins on desk as it was not very stable and accurate with longer distance of camera maybe due to use of an IP camera software (DroidCam - low resolution)
- The SIFT algo was used to detect features for template matching with contrastThreshold=0.01, edgeThreshold=100 params.
- The template to which the coins should be matched were selected very specifically so that SIFT only focuses on the most differentiating features of the 2 selected denominations.
<img width="291" alt="image" src="https://github.com/tusharparimi/coin-counter/assets/93556280/9aa33035-cd48-422c-9bfc-5ddeb4f74491">

### Future improvements
- Extend the detection to more coin denominations and currencies.
