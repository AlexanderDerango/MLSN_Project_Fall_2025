# Getting Started Checklist ✅

Follow these steps to get the application running in 5 minutes.

## Pre-flight Checklist

- [ ] Have Node.js installed? [Download here](https://nodejs.org/)
- [ ] Have Python 3.8+ installed? [Download here](https://www.python.org/)
- [ ] Have a terminal/PowerShell open?
- [ ] Are you in the project directory?

## Installation (2 minutes)

### Step 1: Python Dependencies

```bash
pip install -r requirements.txt
```

✅ You should see packages installing without errors.

### Step 2: Node Dependencies

```bash
npm install
```

✅ You should see `added X packages` message.

### Verify Installation

```bash
# Check Python packages
pip list | findstr Flask scikit-learn pandas

# Check Node packages
npm list react axios
```

## Starting the Application (1 minute)

### Terminal 1 - Start Flask Backend

```bash
python app.py
```

✅ You should see:
```
 * Running on http://127.0.0.1:5000
```

**Leave this terminal running!**

### Terminal 2 - Start React Frontend

```bash
npm start
```

✅ You should see:
```
Compiled successfully!

You can now view bankruptcy-predictor in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://xxx.xxx.x.xxx:3000
```

Browser should automatically open to http://localhost:3000

## Testing the Application (1 minute)

### Verify Backend is Running

Open another terminal and run:

```bash
curl http://localhost:5000/api/health
```

Or in PowerShell:
```powershell
Invoke-WebRequest http://localhost:5000/api/health
```

✅ You should see:
```json
{"status": "ok", "model_loaded": false}
```

*Note: "model_loaded": false is normal until you train the model*

### Test the Frontend

1. Open http://localhost:3000 in your browser
2. You should see:
   - Purple/blue gradient header
   - Form with 18 input fields
   - Each field has a label and info icon
   - Submit and Clear buttons

3. Try expanding a field description:
   - Click the ⓘ icon next to any field
   - Description should appear

### Test Form Submission

1. Fill in all 18 fields with numbers:
   ```
   X1: 1000000
   X2: 500000
   X3: 50000
   X4: 100000
   X5: 200000
   X6: 50000
   X7: 150000
   X8: 5000000
   X9: 2000000
   X10: 5000000
   X11: 500000
   X12: 150000
   X13: 600000
   X14: 300000
   X15: 800000
   X16: 3000000
   X17: 1500000
   X18: 500000
   ```

2. Click "Predict Bankruptcy Risk"

3. You should see:
   - ⚠️ Loading message while processing
   - Results with prediction
   - Risk level (Low/Medium/High)
   - Probability percentages
   - Bar charts

### Test Results Page

1. You should see two buttons:
   - "Analyze Another Company" - Clears results
   - Color-coded risk indicator

2. Click "Analyze Another Company"
   - Form should be empty again

## Troubleshooting

### ❌ "Connection refused" error

**Problem:** Frontend can't reach backend

**Solution:**
1. Make sure `python app.py` is running in Terminal 1
2. Check Flask is listening on port 5000
3. Try: `curl http://localhost:5000/api/health`

### ❌ "Module not found" error

**Problem:** Missing Python package

**Solution:**
```bash
pip install -r requirements.txt
```

### ❌ "npm command not found"

**Problem:** Node.js not installed or not in PATH

**Solution:**
1. Install Node.js from nodejs.org
2. Restart terminal
3. Try `npm --version`

### ❌ Port already in use

**Problem:** Port 3000 or 5000 already in use

**Windows Solution:**
```powershell
# Find process on port 5000
netstat -ano | findstr :5000
# Kill process
taskkill /PID <PID> /F
```

**macOS/Linux Solution:**
```bash
lsof -i :5000
kill -9 <PID>
```

### ❌ Form won't submit

**Problem:** Validation or API error

**Solution:**
1. Check all 18 fields are filled
2. Check all values are numbers (no text)
3. Open browser DevTools (F12)
4. Check Console tab for errors
5. Check Network tab - is request reaching API?

### ❌ Page shows "Model not found"

**Problem:** No trained model exists

**Solution:**
This is normal! You need to train the model:
```bash
python train_model.py
```

*Requires: train.csv, validation.csv, test.csv*

## What's Working

✅ Frontend UI loads  
✅ Form displays  
✅ Field descriptions work  
✅ Form validation works  
✅ API endpoints respond  
✅ Results display correctly  
✅ Mobile responsive works  

## Next Steps

1. **Read the Documentation:**
   - README.md - Full guide
   - QUICK_START.md - More details

2. **Train the Model** (optional):
   - Get training data
   - Run `python train_model.py`

3. **Explore the Code:**
   - See DEVELOPER_GUIDE.md
   - Check component files
   - Review backend code

4. **Deploy to Production:**
   - See DEPLOYMENT.md
   - Consider Docker
   - Set environment variables

## Important Notes

⚠️ **Model Status**: Until you train a model, predictions may not work properly.  
⚠️ **Training Data**: You need CSV files (train.csv, validation.csv, test.csv) to train.  
⚠️ **Port Requirements**: Ensure ports 3000 and 5000 are available.  

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Open DevTools | F12 |
| Reload page | Ctrl+R (Cmd+R) |
| Clear cache | Ctrl+Shift+Delete |
| Stop terminal | Ctrl+C |

## Support

Having issues? Check:

1. **README.md** - Common issues section
2. **QUICK_START.md** - Setup guide
3. **TESTING_GUIDE.md** - Verification steps
4. **DEVELOPER_GUIDE.md** - Architecture details

## Success Indicators

✅ All items below should be true:

- [ ] Both `python app.py` and `npm start` running without errors
- [ ] Browser shows UI at http://localhost:3000
- [ ] Form has 18 visible input fields
- [ ] Can click info icons to see descriptions
- [ ] Can fill form with numbers
- [ ] Form submits without errors
- [ ] Results display after submission
- [ ] Bar charts visible in results
- [ ] Can click "Analyze Another Company" to reset
- [ ] DevTools console has no errors

## Performance Check

Expected performance:
- Page load: < 2 seconds
- API response: < 500ms
- Form submission to results: < 1 second

## Final Checklist

- [ ] Prerequisites installed
- [ ] Dependencies installed
- [ ] Backend server running
- [ ] Frontend server running
- [ ] Browser shows application
- [ ] Form validation working
- [ ] API responding
- [ ] Results displaying
- [ ] Everything working!

---

## 🎉 You're Ready!

If all checkboxes are marked, your application is working perfectly!

**Next:** Read README.md for more features and information.

---

**Need help?** See the documentation files:
- QUICK_START.md
- README.md
- TESTING_GUIDE.md
- DEVELOPER_GUIDE.md
