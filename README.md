# RAG_recipe_and_Nutritional_assistant
# 🥗 NutriBot: Simple Recipe with RAG 

This project implements a Retrieval-Augmented Generation (RAG) system for recipe recommendations and nutritional analysis. It allows users to ask questions like "I have chicken and broccoli, what can I cook under 500 calories?" and get answers based on a specific verified recipe database.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
* **Python 3.8+**
* **API Key** for model

## 🛠️ Installation

1.  **clone Project Folder**
    Create a new folder for your project.
    ```bash
    git clone https://github.com/Meenakshi-Urk24cs1254/RAG_recipe_and_Nutritional_assistant
    cd RAG_recipe_and_Nutritional_assistant
    ```

2.  **Set up a Virtual Environment** (Recommended)
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    We will use `langchain` for orchestration and `chromadb` for the vector store.
    ```bash
    pip install langchain langchain-community chromadb sentence-transformers python-dotenv
    ```

## 📂 Data Preparation

prepare recipe document and save as `recipes.txt`.

**Format your data like this (Clear separation is key):**

```text
RECIPE: Lemon Herb Grilled Chicken
NUTRITION: Calories: 350kcal | Protein: 45g | Carbs: 5g | Fat: 12g
INGREDIENTS: 2 Chicken breasts, 1 lemon, 2 sprigs rosemary, olive oil.
INSTRUCTIONS: Marinate chicken in lemon and herbs for 30 mins. Grill for 6 mins per side. Serve with steamed veggies.
###
RECIPE: Quinoa Power Bowl
NUTRITION: Calories: 420kcal | Protein: 15g | Carbs: 60g | Fat: 18g
INGREDIENTS: 1 cup cooked quinoa, 1/2 avocado, cherry tomatoes, chickpeas, balsamic dressing.
INSTRUCTIONS: Toss all ingredients in a bowl. Drizzle with dressing.
###
