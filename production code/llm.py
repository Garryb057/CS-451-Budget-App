import base64
import json
import requests
from typing import Optional, Dict, List
from datetime import date, datetime
from PIL import Image
import io



class LlamaReceiptReader:
    
    def __init__(self, ollama_host: str = "http://localhost:11434"):
        self.ollama_host = ollama_host
        self.model = "llama3.2-vision"
    
    def encode_image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def read_receipt(self, image_path: str) -> Dict:
        try:
            image_base64 = self.encode_image_to_base64(image_path)
            
            prompt = """Analyze this image carefully.

FIRST: Determine if this is a receipt/invoice. Look for:
- Store/merchant name
- Itemized list of purchases
- Prices and totals
- Date
- Payment information

If this is NOT a receipt (e.g., a photo of a person, landscape, document, meme, etc.), respond with ONLY:
{"is_receipt": false, "reason": "brief explanation of what you see"}

If this IS a receipt but it's too blurry/damaged to read, only get the details you can make out and tell them the image is too blurry, try again.


If this IS a readable receipt, extract the information in this JSON format:
{
    "is_receipt": true,
    "is_readable": true,
    "store_name": "name of the store/merchant",
    "date": "date in YYYY-MM-DD format",
    "total_amount": "total amount as float number only",
    "items": [
        {
            "name": "item name",
            "price": "price as float",
            "quantity": "quantity as integer"
        }
    ],
    "payment_method": "cash/card/other",
    "category_suggestion": "Groceries/Dining Out/Entertainment/Transportation/Utilities/Healthcare/Shopping/Other",
    "confidence": "high/medium/low - your confidence in the extraction"
}

IMPORTANT: 
- Return ONLY valid JSON, no markdown, no extra text
- Use null for missing information
- Be honest about image quality and readability"""

            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "images": [image_base64],
                    "stream": False,
                    "format": "json"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                receipt_data = json.loads(result['response'])
                return self._validate_and_clean_receipt_data(receipt_data)
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Failed to read receipt: {str(e)}"}
    
    def _validate_and_clean_receipt_data(self, data: Dict) -> Dict:
        cleaned = {
            "store_name": data.get("store_name", "Unknown"),
            "date": self._parse_date(data.get("date")),
            "total_amount": self._parse_amount(data.get("total_amount")),
            "items": data.get("items", []),
            "payment_method": data.get("payment_method", "unknown"),
            "category_suggestion": data.get("category_suggestion", "Other")
        }
        return cleaned
    
    def _parse_date(self, date_str: str) -> date:
        if not date_str:
            return date.today()
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            return date.today()
    
    def _parse_amount(self, amount) -> float:
        try:
            if isinstance(amount, str):
                amount = amount.replace('$', '').replace(',', '').strip()
            return float(amount)
        except:
            return 0.0
    
    def get_receipt_summary(self, image_path: str) -> str:
        receipt_data = self.read_receipt(image_path)
        
        if "error" in receipt_data:
            return f"Error: {receipt_data['error']}"
        
        summary = f"""Receipt Summary:
        Store: {receipt_data['store_name']}
        Date: {receipt_data['date']}
        Total: ${receipt_data['total_amount']:.2f}
        Suggested Category: {receipt_data['category_suggestion']}
        Payment: {receipt_data['payment_method']}

        Items:"""
        
        for item in receipt_data.get('items', []):
            summary += f"\n  - {item.get('name', 'Unknown')}: ${item.get('price', 0):.2f}"
        
        return summary


class LlamaBudgetChatbot:
    
    def __init__(self, ollama_host: str = "http://localhost:11434", user_context: Dict = None):
        self.ollama_host = ollama_host
        self.model = "budgetBot"
        self.conversation_history: List[Dict] = []
        self.user_context = user_context or {}
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:

        base_prompt = """You are BudgetBot, an AI financial advisor assistant integrated into a personal budgeting application.

        YOUR ROLE:
        You help users manage their personal finances through:
        - Analyzing spending patterns and identifying trends
        - Providing budget recommendations (50/30/20 rule, zero-based budgeting, etc.)
        - Suggesting ways to save money and reduce expenses
        - Helping categorize transactions
        - Explaining financial concepts in simple, clear language
        - Giving bill reminders and financial tips

        YOUR PERSONALITY:
        - Friendly, supportive, and never judgmental about past spending
        - Enthusiastic about helping users achieve their financial goals
        - Speak conversationally, like a helpful friend who knows about money

        YOUR GUIDELINES:
        1. Keep responses concise (2-4 sentences) unless user asks for detailed explanation
        2. Always provide ACTIONABLE advice, not just theory
        3. When you see concerning spending patterns, point them out gently
        4. End responses with a follow-up question or suggestion when helpful
        5. If you don't have specific user data, say so clearly and suggest where they can find it
        6. Focus on budgeting and spending management - NOT investment advice or tax advice

        IMPORTANT LIMITATIONS:
        - You are NOT a licensed financial advisor, tax professional, or investment advisor
        - You provide budgeting guidance only, not legal or tax advice
        - Always remind users to consult professionals for serious financial decisions"""

        if self.user_context:
            base_prompt += "\n\n=== USER'S FINANCIAL CONTEXT ===\n"
            base_prompt += "Use this information to give PERSONALIZED advice:\n\n"
        
        if "first_name" in self.user_context:
            base_prompt += f"- User's name: {self.user_context['first_name']}\n"
        
        if "monthly_income" in self.user_context:
            income = self.user_context['monthly_income']
            base_prompt += f"- Monthly Income: ${income:,.2f}\n"
            base_prompt += f"  * Suggested savings (20%): ${income * 0.20:,.2f}\n"
            base_prompt += f"  * Needs budget (50%): ${income * 0.50:,.2f}\n"
            base_prompt += f"  * Wants budget (30%): ${income * 0.30:,.2f}\n"
        
        if "current_balance" in self.user_context:
            base_prompt += f"- Current Balance: ${self.user_context['current_balance']:,.2f}\n"
        
        if "budget_total" in self.user_context:
            base_prompt += f"- Total Monthly Budget: ${self.user_context['budget_total']:,.2f}\n"
        
        if "spending_this_month" in self.user_context:
            spent = self.user_context['spending_this_month']
            budget = self.user_context.get('budget_total', 0)
            if budget > 0:
                percentage = (spent / budget) * 100
                base_prompt += f"- Spent This Month: ${spent:,.2f} ({percentage:.1f}% of budget)\n"
            else:
                base_prompt += f"- Spent This Month: ${spent:,.2f}\n"
        
        if "top_spending_category" in self.user_context:
            base_prompt += f"- Top Spending Category: {self.user_context['top_spending_category']}\n"
        
        base_prompt += "\n=== END USER CONTEXT ===\n"
        base_prompt += "\nUse the above data to give SPECIFIC, PERSONALIZED advice. Reference actual numbers when relevant.\n"
    
        return base_prompt
    
    def update_user_context(self, context: Dict):
        self.user_context.update(context)
        self.system_prompt = self._build_system_prompt()
    
    def chat(self, user_message: str, include_history: bool = True) -> str:
        try:
            messages = []
            
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
            
            if include_history:
                messages.extend(self.conversation_history)
            
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            response = requests.post(
                f"{self.ollama_host}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result['message']['content']
                
                self.conversation_history.append({
                    "role": "user",
                    "content": user_message
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
                
                return assistant_message
            else:
                return f"Error: Unable to get response (Status: {response.status_code})"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_spending_insights(self, transactions: List[Dict]) -> str:
        total_spent = sum(t.get('amount', 0) for t in transactions)
        categories = {}
        
        for trans in transactions:
            cat = trans.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + trans.get('amount', 0)
        
        summary = f"Total spent: ${total_spent:.2f}\n"
        summary += "Spending by category:\n"
        for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_spent * 100) if total_spent > 0 else 0
            summary += f"- {cat}: ${amount:.2f} ({percentage:.1f}%)\n"
        
        prompt = f"""Based on this spending data:

        {summary}

        Provide:
        1. Key insights about spending patterns
        2. Areas of concern or overspending
        3. 2-3 actionable recommendations to improve financial health

        Keep it concise and specific."""

        return self.chat(prompt, include_history=False)
    
    def suggest_budget_allocation(self, monthly_income: float, expenses: Dict[str, float]) -> str:
        expense_summary = "\n".join([f"- {cat}: ${amt:.2f}" for cat, amt in expenses.items()])
        
        prompt = f"""I have a monthly income of ${monthly_income:.2f}.

        My current expense allocation:
        {expense_summary}

        Based on the 50/30/20 rule and best practices, suggest an optimal budget allocation. 
        Provide specific dollar amounts for each category."""

        return self.chat(prompt, include_history=False)
    
    def clear_history(self):
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict]:
        return self.conversation_history.copy()


class BudgetAssistantManager:
    
    def __init__(self, ollama_host: str = "http://localhost:11434"):
        self.receipt_reader = LlamaReceiptReader(ollama_host)
        self.chatbot = None
        self.ollama_host = ollama_host
    
    def initialize_chatbot(self, user_id: str, user_context: Dict = None):
        self.chatbot = LlamaBudgetChatbot(self.ollama_host, user_context)
        return self.chatbot
    
    def process_receipt_and_create_transaction(self, image_path: str, user_id: str, 
                                               transaction_manager, category_map: Dict[str, int]) -> Dict:
        receipt_data = self.receipt_reader.read_receipt(image_path)
        
        if "error" in receipt_data:
            return receipt_data
        
        suggested_cat = receipt_data.get('category_suggestion', 'Other')
        category_id = category_map.get(suggested_cat, category_map.get('Other', 1))
        
        from Money import Transaction, ExpenseType
        
        transaction = Transaction(
            transactionID=len(transaction_manager.transactions) + 1,
            userID=user_id,
            total=receipt_data['total_amount'],
            date=receipt_data['date'],
            payee=receipt_data['store_name'],
            categoryID=category_id,
            notes=f"Auto-imported from receipt. Payment: {receipt_data['payment_method']}",
            isRecurring=False,
            expenseType=ExpenseType.VARIABLE
        )
        
        transaction_manager.add_transaction(transaction)
        
        return {
            "success": True,
            "transaction": transaction,
            "receipt_data": receipt_data,
            "message": f"Transaction created: ${receipt_data['total_amount']:.2f} at {receipt_data['store_name']}"
        }
    
    def ask_budget_question(self, question: str) -> str:
        if not self.chatbot:
            return "Chatbot not initialized. Please call initialize_chatbot() first."
        return self.chatbot.chat(question)
    
    def get_smart_insights(self, user_data: Dict) -> Dict[str, str]:
        if not self.chatbot:
            return {"error": "Chatbot not initialized"}
        
        insights = {}

        if "transactions" in user_data:
            insights["spending_analysis"] = self.chatbot.get_spending_insights(
                user_data["transactions"]
            )
        if "monthly_income" in user_data and "expenses" in user_data:
            insights["budget_suggestions"] = self.chatbot.suggest_budget_allocation(
                user_data["monthly_income"],
                user_data["expenses"]
            )
        
        return insights