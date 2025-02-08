# 🎯 ValChecker  

ValChecker is a Python-based tool designed to verify the validity of Valorant accounts with multi-threading, proxy support, and Discord webhook integration.  

🚀 **Latest Update:** Re-written the original repo, since its creator stopped its development. Any report and/or contribution is highly appreciated.

---

## 📜 Table of Contents  
- [🔥 Overview](#-overview)  
- [⚙️ How to Install](#-how-to-install)  
- [🚀 Running the Tool](#-running-the-tool)  
- [💡 Troubleshooting Tips](#-troubleshooting-tips)  
- [💻 Contributing](#-contributing)  
- [📜 License & Terms](#-license--terms)  
- [⚠️ Important Notice](#-important-notice)  

---

## 🔥 Overview  

✔️ **Multi-Threading:** Efficiently processes multiple accounts in parallel.  
✔️ **Proxy Support:** Anonymize your checks using proxy integration.  
✔️ **Discord Webhook Integration:** Get real-time results in a Discord channel.  
✔️ **User-Friendly:** Simple and clear command-line interface (CLI).  

---

## ⚙️ How to Install  

### 1️⃣ Clone the repository:  
```bash
git clone https://github.com/smokeytempo/valchecker.git
cd valchecker
```  

### 2️⃣ Install dependencies:  
Ensure you have Python **3.x** installed, then run:  
```bash
pip install -r requirements.txt
```  

---

## 🚀 Running the Tool  

### 1️⃣ Configure Proxies  
Edit `data/proxies.txt` and add your proxies:  
```plaintext
http://username:password@proxy_address:port
```  

### 2️⃣ Run ValChecker  
Execute the main script:  
```bash
python -m src.main
```  

### ✅ Results:  
- ✅ **Valid accounts:** `output/valid_accounts.txt`  
- ❌ **Invalid accounts:** `output/invalid_accounts.txt`  

---

## 💡 Troubleshooting Tips  

### ❌ `ModuleNotFoundError: No module named 'src'`  
✔️ **Fix:** Run the script using:  
```bash
python -m src.main
```  

✔️ **Or manually set the path:**  
```bash
export PYTHONPATH=$(pwd)
python src/main.py
```  

### ❌ Issues with Dependencies?  
Ensure all required packages are installed:  
```bash
pip install -r requirements.txt
```  

---

## 💻 Contributing  

We welcome contributions! Follow these steps:  

1. **Fork the repository**  
2. **Create a feature branch:** `git checkout -b feature-name`  
3. **Commit your changes:** `git commit -m "Add new feature"`  
4. **Push to GitHub:** `git push origin feature-name`  
5. **Submit a Pull Request** 🚀  

---

## 📜 License & Terms  

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.  

---

## ⚠️ Important Notice  

> ⚠️ **Warning:** This tool is deprecated and may no longer function due to Valorant's captcha protection.  
> **Use at your own risk!**  

💖 **Found this project helpful?** Leave a ⭐ on GitHub!  
