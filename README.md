# 🌾 AgriSwap



AgriSwap is a web-based platform designed to bridge the gap between **farmers** and **customers** by enabling product **swapping**, **buying**, and **plant disease detection**. Built with Django, it offers a seamless experience to manage agricultural products and promote direct interaction within the ecosystem.

---

## 📌 Problem Statement

- Lack of a unified marketplace for farmers to trade or swap products.
- Difficulty for customers to access fresh produce directly from farmers.
- Limited access to early plant disease detection tools in rural areas.
- Unfare practices on pricing including commissions for mediators.
- Farmers forced to sell products due to expiry.

---

## 🎯 Objectives

- Enable product swapping among farmers.
- Provide an intuitive platform for customers to buy products.
- Integrate a plant disease detection tool for farmers.
- Manage and verify users through an admin dashboard.
- removing mediators and provide direct purchasing of products

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript, SCSS  
- **Backend**: Python, Django  
- **Database**: SQLite  
- **Tools**: Django Admin, Image Upload, File Handling

---

## 📁 Project Structure

```
AgriSwap/
├── AgriSwap/
├── Basic/
├── Customer/
├── Farmer/
├── Guest/
├── Assets/
├── static/uploads/
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

## ⚙️ Installation (Local Setup)

### 1. Clone the Repository

```bash
git clone https://github.com/jeraldmathewsjomy/AgriSwap.git
cd AgriSwap
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🚀 Feature Demonstration

### 👨‍🌾 Farmer: Product Swapping

Follow these steps to swap products with other farmers:

1. **Login as Farmer**  
   Navigate to `/farmerlogin` and enter your credentials.


   ![Login Page](https://github.com/user-attachments/assets/e840ea70-c7a4-4ac4-983e-cd2ddbb71520)

2. **Access Dashboard**  
   After logging in, you will be redirected to the Farmer Dashboard.

   
   ![Farmer Dashboard](https://github.com/user-attachments/assets/89174277-be5a-4d9a-8b1c-af616466435d)

3. **Click "Add Product"**  
   Select the option to add a new product for listing.

   
   ![Add Product](https://github.com/user-attachments/assets/8aefbe68-ea10-4eee-9306-64ccfed5862e)

4. **Enter Product Stock**  
   Provide the quantity available in stock.

   
   ![Enter Stock](https://github.com/user-attachments/assets/aa2a7819-77e4-49bd-94c8-3dba035f5f88)

5. **Click "Swap"**  
   Open the swap interface by clicking the "Swap" button next to the listed product.

   
   ![Click Swap](https://github.com/user-attachments/assets/b9d67629-dbd7-4204-a559-d1d72cbcae07)

6. **Send Swap Request**  
   Enter the desired quantity to swap and click the **Send Request** button.


   ![Send Swap Request](https://github.com/user-attachments/assets/991d098e-6b87-4165-bf9f-31053fd9365b)

7. **Manage Incoming Requests**  
   View and respond to incoming swap requests from other farmers. Accept or reject as needed.


   ![View Swap Requests](https://github.com/user-attachments/assets/5782a90b-d8fa-4c93-93b8-233ce6288a74)  
   ![Respond to Swap](https://github.com/user-attachments/assets/2f6ff269-7350-4d28-8b67-3de711360f65)


### 🌿 Farmer: Plant Disease Detection

1. Navigate to Disease Prediction.

     ![Screenshot 2025-04-12 124343](https://github.com/user-attachments/assets/dcd7fe9d-6d7c-4ca1-9edf-a08460ac77ad)

2. Upload a plant or leaf image.

     ![Screenshot 2025-04-12 124425](https://github.com/user-attachments/assets/5c85b05e-21a6-4fc1-9e7f-382ba8b6e282)

3. System displays predicted disease and accuracy.

     ![Screenshot 2025-04-12 124445](https://github.com/user-attachments/assets/e02bd8b5-5c03-4a0a-90cc-2217ef9cbecb)



---

### 👥 Customer: Product Buying

1. Login via `/customerlogin` into Dashboard.

    ![Screenshot 2025-04-12 141742](https://github.com/user-attachments/assets/15ed7b15-289b-4554-ad26-b70168500d45)

3. Browse available products.

     ![Screenshot 2025-04-12 141751](https://github.com/user-attachments/assets/2b9c50f0-90ed-451a-98c2-cf95676b9658)

5. Add to cart and checkout.

     ![Screenshot 2025-04-12 141807](https://github.com/user-attachments/assets/1c2cd0fb-595c-41ae-99f8-9e30aae1b7cc)
     ![Screenshot 2025-04-12 141815](https://github.com/user-attachments/assets/ab860b0d-3287-499a-b1b6-f0ce79cfc067)


---

### 🧑‍💼 Admin: Management Dashboard

1. Login via `/adminlogin`.

    ![Screenshot 2025-04-12 142841](https://github.com/user-attachments/assets/54463015-aaa2-4083-88be-b42b495edf11)

2. Add List of Products to be available to sell in this platform.

    ![Screenshot 2025-04-12 142900](https://github.com/user-attachments/assets/9f7c38c0-9fdc-4e66-82aa-397c59a91188)

3. Approve or reject farmer and customer accounts.

    ![Screenshot 2025-04-12 142946](https://github.com/user-attachments/assets/e1b9882b-6983-4caa-9d42-7bc09f559ddf)


---



## 📱 Mobile Version Screenshots


Below are mobile views of key features for a responsive experience:




<div align="center">

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/2e462e4f-6f9a-4995-b926-31d55de88bbf" width="200"/></td>
    <td><img src="https://github.com/user-attachments/assets/967a6c07-e414-4b6b-9f23-3b06e3c7a11f" width="200"/></td>
    <td><img src="https://github.com/user-attachments/assets/dec82f70-ff6c-4136-8458-152455d14a7d" width="200"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/1cf1f85c-e6ff-463f-8765-d8fc490e54da" width="200"/></td>
    <td><img src="https://github.com/user-attachments/assets/f5d73a13-7474-4609-b8e1-82589b7dec78" width="200"/></td>
    <td><img src="https://github.com/user-attachments/assets/aef0f9af-7ccb-42ca-a487-0246fe825474" width="200"/></td>
  </tr>
</table>

</div>



---

## 🔮 Future Enhancements

- Add payment gateway.
- Real-time messaging between users.

---

## 👨‍💻 Author

Developed by Jerald Mathews Jomy , Judin Jimmy , Johan Joe , Kevin Sunny

---

## 📃 License

This project is for demonstration and educational use only.
