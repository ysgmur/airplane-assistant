# ✈️ Airline AI Assistant

A conversational assistant that allows users to search flights, buy tickets, and check in via chat.  
Frontend built with React, real-time messaging via Firebase, backend handled by Flask API + OpenAI.

---

## 🔗 Source Code

GitHub Repo: [https://github.com/ysgmur/airplane-assistant](https://github.com/ysgmur/airplane-assistant)

---

## 🛠️ Design

- **Frontend:** React SPA using `useState`, `useEffect`, Axios
- **Backend:** Flask REST API with `/auth/login`, `/flights`, `/buy`, `/checkin` endpoints
- **Authentication:** JWT-based token stored in `localStorage`
- **Database:** Firebase Firestore for real-time chat
- **AI Integration:** User messages parsed via OpenAI API to identify intent and parameters

---

## ✅ Assumptions

- The user sends plain text messages (e.g., “I want to book a flight from Izmir to Rome on June 10”)
- Each message is saved to Firestore with a JWT token and timestamp
- A backend service parses intent, calls related endpoints, and sends structured response back
- Token validation is required for protected actions like buying or checking in
- The app assumes backend is running locally at `http://localhost:10000/api/v1`

---

## ⚠️ Issues Encountered

- ❌ **Push Protection Errors:** Initial commits accidentally included secrets (.env and Firebase key)
- ✅ **Solved by:** Creating a `.gitignore` and doing a clean re-push without secrets
- ❌ **Firebase Misconfig:** Used `serviceAccount` key instead of `web app config` in frontend
- ✅ **Solved by:** Replacing with Firebase Web Config in `firebase_config.js`
- ❌ **Login Failing:** React was pointing to wrong API port in `.env`
- ✅ **Solved by:** Updating `REACT_APP_API_URL=http://localhost:10000/api/v1`
- ❌ **OPTIONS 200 but no response:** CORS was missing
- ✅ **Solved by:** Adding `flask-cors` and enabling CORS in backend

---

## 📦 Sample `.env` (DO NOT PUSH)

```env
REACT_APP_API_URL=http://localhost:10000/api/v1
