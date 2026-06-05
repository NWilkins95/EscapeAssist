# Question ID: 32
**Question:**  
What should you do if the engine coolant temperature warning light illuminates?

---

## Version V0

### V0 Answer
If the engine coolant temperature warning light illuminates, follow these steps:

1. **Pull Off the Road**: Safely bring your vehicle to a stop as soon as possible.  
2. **Switch Off the Engine**: Turn off the engine to prevent further overheating.  
3. **Wait for Cooling**: Allow the engine to cool down for a short period.  
4. **Check Coolant Level**: Inspect the coolant level in the reservoir. If it is at or below the minimum mark, add prediluted coolant immediately.  
5. **Restart the Engine**: Once the engine has cooled, you can restart it. Monitor the temperature gauge closely.  
6. **Seek Repairs**: Have your vehicle checked as soon as possible to minimize the risk of engine damage.

**Important Note**: Do not remove the coolant reservoir cap when the engine is hot, as this can cause scalding.

### Human Scores (V0)
- Correctness: 2  
- Grounding: 2  
- Hallucination: 4  
- Refusal Quality: N/A  

**Notes:**  
- The manual’s instruction is simple: stop, turn off the vehicle, and get it checked.  
- The model invents a multi-step diagnostic procedure not found in the source.  
- Recommending checking coolant level and adding coolant is **dangerous** unless the system is fully cooled.  
- These hallucinations contradict Ford safety guidance → severity = 4.

### Judge Scores (V0)
- Correctness: 3  
- Grounding: 3  
- Hallucination: true  
- Refusal Quality: N/A  

### Comparison Summary (V0)
- Match: partial  
- Disagreement Type: correctness, grounding  
- Needs disagreement log: yes  

---

## Version V1

### V1 Answer
If the engine coolant temperature warning light illuminates, follow these steps:

1. **Pull Off the Road**: Safely stop your vehicle as soon as possible and switch off the engine.  
2. **Contact Roadside Assistance**: If you have a roadside assistance program, consider contacting them for help.  
3. **Wait for Cooling**: If roadside assistance is not an option, wait a short period for the engine to cool down.  
4. **Check Coolant Level**: After the engine has cooled, check the coolant level in the reservoir.  
   - If the coolant level is at or below the minimum mark, add prediluted coolant immediately.  
5. **Restart the Engine**: Once the engine has cooled and the coolant level is adequate, you can restart the engine.  
6. **Seek Professional Help**: Have your vehicle checked as soon as possible to prevent potential engine damage.

### Human Scores (V1)
- Correctness: 2  
- Grounding: 2  
- Hallucination: 4  
- Refusal Quality: N/A  

**Notes:**  
- Same dangerous hallucinations as V0: checking coolant, adding coolant, restarting engine.  
- None of these steps appear in the manual.  
- The model again contradicts Ford’s safety guidance.

### Judge Scores (V1)
- Correctness: 3  
- Grounding: 3  
- Hallucination: true  
- Refusal Quality: N/A  

### Comparison Summary (V1)
- Match: partial  
- Disagreement Type: correctness, grounding 
- Needs disagreement log: yes  

---

## Version V2

### V2 Answer
If the engine coolant temperature warning light illuminates, follow these steps:

1. **Stop Safely**: Pull off the road as soon as it is safe to do so. Fully apply the parking brake and shift into park (P) or neutral (N).  
2. **Leave Engine Running**: Keep the engine running until the coolant temperature gauge returns to the normal position.  
3. **Turn Off Engine**: Switch off the engine and wait for it to cool down.  
4. **Check Coolant Level**: Inspect the coolant level in the reservoir.  
5. **Add Coolant if Necessary**: If the coolant level is at or below the minimum mark, add prediluted coolant immediately.  
6. **Restart Engine**: Once the engine has cooled, you can restart it. Have your vehicle checked as soon as possible.

### Human Scores (V2)
- Correctness: 1  
- Grounding: 1  
- Hallucination: 4  
- Refusal Quality: N/A  

**Notes:**  
- This version is even more dangerous: it recommends **leaving the engine running**, which directly contradicts the manual.  
- Again invents steps about checking coolant and adding coolant.  
- High-severity hallucination due to unsafe mechanical advice.

### Judge Scores (V2)
- Correctness: 3  
- Grounding: 3  
- Hallucination: true  
- Refusal Quality: N/A  

### Comparison Summary (V2)
- Match: partial  
- Disagreement Type: correctness, grounding 
- Needs disagreement log: yes  

---

# Overall Notes for This Question
- The manual’s instruction is extremely simple:  
  **“Safely stop your vehicle and switch your vehicle off. Have your vehicle checked as soon as possible.”**  
- All three versions invent multi-step troubleshooting procedures that do **not** appear in the source.  
- All versions include **dangerous mechanical hallucinations**, especially recommending adding coolant on a vehicle that is not completely cooled.  
- V2 is the most unsafe, recommending leaving the engine running.  
