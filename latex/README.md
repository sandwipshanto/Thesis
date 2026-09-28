# Quick Start Guide - Compile Your Thesis

## Step 1: Install MiKTeX (5 minutes)

### Option A: Automated (if download completes)
The installer should launch automatically. Follow these steps:

1. ✅ **Click "Next"** on welcome screen
2. ✅ **Accept license** → Click "Next"
3. ✅ **Choose "Install for all users"** (recommended) or "Just for me"
4. ✅ **Installation Directory**: Keep default → Click "Next"
5. ✅ **Settings**:
   - ⚠️ **IMPORTANT**: Set **"Install missing packages"** to **"Yes"** (not "Ask me first")
   - This allows automatic package installation during compilation
6. ✅ Click **"Start"** and wait (5-10 minutes)
7. ✅ Click **"Close"** when done

### Option B: Manual Download (if automated fails)
1. Visit: https://miktex.org/download
2. Click **"Download Basic MiKTeX Installer"** (Windows x64)
3. Run the downloaded `.exe` file
4. Follow steps above

---

## Step 2: Verify Installation

Close and reopen PowerShell, then run:
```powershell
pdflatex --version
```

You should see: `MiKTeX-pdfTeX 4.x...`

---

## Step 3: Compile Thesis (2-3 minutes)

Simply run:
```powershell
.\compile_thesis.ps1
```

This will:
- ✅ Run pdfLaTeX (1st pass)
- ✅ Run BibTeX (bibliography)
- ✅ Run pdfLaTeX (2nd pass - resolve references)
- ✅ Run pdfLaTeX (3rd pass - finalize)
- ✅ Open `thesis.pdf` automatically

**Expected output:** 
- File: `thesis.pdf` 
- Size: ~1-2 MB
- Pages: ~200-300

---

## What to Expect During Compilation

### First Compilation:
```
STEP 1/4: First pdfLaTeX compilation...
This may take 1-2 minutes and will show many warnings - this is normal!
```

**If you see package installation prompts:**
- MiKTeX will ask to install packages (first time only)
- Click **"Install"** for each package
- This is normal and expected

### Compilation Progress:
```
STEP 2/4: Running BibTeX (processing bibliography)...
✅ BibTeX completed!

STEP 3/4: Second pdfLaTeX compilation (resolving references)...
✅ Second compilation completed!

STEP 4/4: Third pdfLaTeX compilation (finalizing)...
✅ Third compilation completed!

🎉 SUCCESS! PDF generated successfully!
📄 File: thesis.pdf
📊 Size: 1.23 MB
```

---

## Troubleshooting

### Problem: "pdflatex not recognized"
**Solution:** 
1. Close PowerShell completely
2. Reopen PowerShell
3. Try again (PATH needs to refresh)

### Problem: Package installation dialogs keep appearing
**Solution:**
- Click "Install" for each package
- Or: Run MiKTeX Console → Settings → Set "Install packages on-the-fly" to "Yes"

### Problem: Compilation fails with errors
**Solution:**
1. Check `thesis.log` file:
   ```powershell
   Get-Content thesis.log -Tail 50
   ```
2. Look for lines starting with `!` (errors)
3. Share the error message with me

### Problem: Bibliography not showing
**Solution:**
- This is normal on first compile
- The script runs 3 compilations to fix this
- If still missing after 3rd compile, run the script again

---

## File Structure After Compilation

```
Thesis-1/
├── thesis.pdf          ← YOUR COMPILED PDF! ✅
├── thesis.tex          ← Main file
├── references.bib      ← Bibliography
├── chapters/           ← All chapter files
│
├── thesis.aux          ← Temporary (can delete)
├── thesis.log          ← Build log (can delete)
├── thesis.toc          ← Table of contents data (can delete)
├── thesis.lot          ← List of tables data (can delete)
├── thesis.lof          ← List of figures data (can delete)
├── thesis.bbl          ← Bibliography data (can delete)
├── thesis.blg          ← BibTeX log (can delete)
└── thesis.out          ← Hyperref data (can delete)
```

To clean temporary files:
```powershell
.\clean_build.ps1
```

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| Compile thesis | `.\compile_thesis.ps1` |
| Clean temp files | `.\clean_build.ps1` |
| View PDF | `thesis.pdf` (double-click) |
| Check LaTeX | `pdflatex --version` |
| View last 50 log lines | `Get-Content thesis.log -Tail 50` |

---

## Next Steps After First Successful Compilation

1. ✅ Review PDF - check all chapters appear
2. ✅ Check table of contents
3. ✅ Verify bibliography shows all references
4. ✅ Review formatting (margins, spacing, fonts)

---

## Need Help?

**Common issues solved:**
- 95% of problems: Close and reopen PowerShell
- Package errors: Click "Install" when prompted
- Bibliography missing: Run compile script again

**Still stuck?** Share:
1. The exact error message
2. Last 20 lines from `thesis.log`
3. Which step failed

---

**Estimated total time:** 15-20 minutes (including MiKTeX installation)

Good luck! 🎓
