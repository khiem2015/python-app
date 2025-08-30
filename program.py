from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import sys
from data_io import *
from weather_api import *

class Alert(QMessageBox):
    def error_message(self, title, message):
        self.setIcon(QMessageBox.Icon.Critical)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()
    def success_message(self, title, message):
        self.setIcon(QMessageBox.Icon.Information)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()


class Login(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)

        self.email_input = self.findChild(QLineEdit, "txt_email")
        self.password_input = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_eye = self.findChild(QPushButton, "btn_eye")

        self.btn_eye.clicked.connect(lambda: self.show_password(self.btn_eye, self.password_input))
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)

    def show_password(self, button: QPushButton, input: QLineEdit):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))

    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if email == "":
            msg.error_message("Login", "Email is required")
            self.email_input.setFocus()
            return
        
        if password == "":
            msg.error_message("Login", "Password is required")
            self.password_input.setFocus()
            return
                
        user = get_user_by_email_and_password(email, password)
        if user:
            msg.success_message("Login", "Welcome to the system")
            self.show_home(user["id"])
            return
                
        msg.error_message("Login", "Invalid email or password")
        self.email_input.setFocus()

    def show_register(self):
        self.register = Register()
        self.register.show()
        self.hide()
    
    def show_home(self, id):
        self.home = Home(id)
        self.home.show()
        self.hide()

class Register(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)

        self.email_input = self.findChild(QLineEdit, "txt_email")
        self.password_input = self.findChild(QLineEdit, "txt_password")
        self.name_input = self.findChild(QLineEdit, "txt_name")
        self.confirm_pass_input = self.findChild(QLineEdit, "txt_confirm_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")
        self.btn_eye_cp = self.findChild(QPushButton, "btn_eye_cp")

        self.btn_eye_p.clicked.connect(lambda: self.show_password(self.btn_eye_p, self.password_input))
        self.btn_eye_cp.clicked.connect(lambda: self.show_password(self.btn_eye_cp, self.confirm_pass_input))
        self.btn_register.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.show_login)

    def show_password(self, button: QPushButton, input: QLineEdit):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))
            
    def register(self):
        email = self.email_input.text().strip()
        name = self.name_input.text().strip()
        password = self.password_input.text().strip()
        confirm_pass = self.confirm_pass_input.text().strip()
        
        if email == "":
            msg.error_message("Register", "Email is required")
            self.email_input.setFocus()
            return
        
        if name == "":
            msg.error_message("Register", "Name is required")
            self.name_input.setFocus()
            return
        
        if password == "":
            msg.error_message("Register", "Password is required")
            self.password_input.setFocus()
            return
            
        if confirm_pass == "":
            msg.error_message("Register", "Confirm password is required")
            self.confirm_pass_input.setFocus()
            return
        
        if password != confirm_pass:
            msg.error_message("Register", "Password and confirm password do not match")
            self.password_input.setFocus()
            return
        
        user = get_user_by_email(email)
        if user:
            msg.error_message("Register", "Email already exists")
            self.email_input.setFocus()
            return

        create_user(email, password, name)   
                
        with open("data/users.txt", "a") as file:
            file.write(f"{email},{password},{name}\n")

        msg.success_message("Register", "Account created successfully")
        self.show_login()

    def show_login(self):
        self.login = Login()
        self.login.show()
        self.hide()

class Home(QWidget):
    def __init__(self, id):
        super().__init__()
        uic.loadUi("ui/home.ui", self)

        self.id = id
        self.user = get_user_by_id(id)
        self.current_city = "Ho Chi Minh City"
        self.load_user_info()
        self.setup_weather_ui()
        self.load_weather_data()
        
        self.stack_widget = self.findChild(QStackedWidget, "stackedWidget")
        self.btn_home = self.findChild(QPushButton, "btn_home")
        self.btn_profile = self.findChild(QPushButton, "btn_profile")
        self.btn_detail = self.findChild(QPushButton, "btn_detail")
        self.btn_save_account = self.findChild(QPushButton, "btn_save_account")

        self.txt_name = self.findChild(QLineEdit, "txt_name")
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_birthday = self.findChild(QDateEdit, "txt_birthday")
        self.txt_gender = self.findChild(QComboBox, "txt_gender")
        self.btn_avatar = self.findChild(QPushButton, "btn_avatar")
        
        # Weather UI elements
        self.txt_search = self.findChild(QLineEdit, "txt_search")
        self.label_city_name = self.findChild(QLabel, "label_city_name")
        self.label_current_temp = self.findChild(QLabel, "label_current_temp")
        self.label_current_day = self.findChild(QLabel, "label_current_day")

        self.btn_home.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 0))
        self.btn_profile.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 1))
        self.btn_save_account.clicked.connect(self.update_user_info)
        self.btn_avatar.clicked.connect(self.update_avatar)
        
        # Connect search functionality
        self.txt_search.returnPressed.connect(self.search_weather)

    def setup_weather_ui(self):
        """Setup weather UI elements with proper naming"""
        self.weather_frames = []
        self.weather_labels = {}
        
        # Get all weather frame elements
        for i in range(1, 6):  # 5 days
            frame = self.findChild(QFrame, f"frame_day{i}")
            if frame:
                self.weather_frames.append(frame)
                
                # Get labels for each day
                day_name = self.findChild(QLabel, f"label_day_name{i}")
                weather_desc = self.findChild(QLabel, f"label_weather_day{i}")
                temp = self.findChild(QLabel, f"label_temp_day{i}")
                details = self.findChild(QLabel, f"label_details_day{i}")
                icon_btn = self.findChild(QPushButton, f"btn_icon_day{i}")
                
                if all([day_name, weather_desc, temp, details, icon_btn]):
                    self.weather_labels[i] = {
                        'day_name': day_name,
                        'weather_desc': weather_desc,
                        'temp': temp,
                        'details': details,
                        'icon_btn': icon_btn
                    }

    def search_weather(self):
        """Search for weather by city name"""
        city = self.txt_search.text().strip()
        if city:
            self.current_city = city
            self.load_weather_data()
            self.txt_search.clear()

    def load_weather_data(self):
        """Load weather data from API"""
        try:
            # Get current weather
            current_weather = get_weather_by_name(self.current_city)
            if current_weather and current_weather.get('cod') == 200:
                self.update_current_weather(current_weather)
            
            # Get 5-day forecast
            forecast = get_weather_forecast_by_name(self.current_city)
            if forecast and forecast.get('cod') == '200':
                self.update_forecast(forecast)
                
        except Exception as e:
            print(f"Error loading weather data: {e}")

    def update_current_weather(self, weather_data):
        """Update current weather display"""
        try:
            # Update city name
            self.label_city_name.setText(self.current_city)
            
            # Update temperature
            temp = weather_data['main']['temp']
            self.label_current_temp.setText(f"{int(temp)}°C")
            
            # Update current day
            from datetime import datetime
            current_day = datetime.now().strftime('%A')
            self.label_current_day.setText(current_day)
            
        except Exception as e:
            print(f"Error updating current weather: {e}")

    def update_forecast(self, forecast_data):
        """Update 5-day forecast display"""
        try:
            # Group forecasts by day
            daily_forecasts = {}
            
            for item in forecast_data['list']:
                from datetime import datetime
                dt = datetime.fromtimestamp(item['dt'])
                date_key = dt.strftime('%Y-%m-%d')
                
                if date_key not in daily_forecasts:
                    daily_forecasts[date_key] = {
                        'date': dt,
                        'day_name': dt.strftime('%A'),
                        'temp_min': float('inf'),
                        'temp_max': float('-inf'),
                        'weather_main': item['weather'][0]['main'],
                        'weather_desc': item['weather'][0]['description'],
                        'humidity': item['main']['humidity'],
                        'wind_speed': item['wind']['speed'],
                        'pop': item.get('pop', 0) * 100
                    }
                
                # Update min/max temperatures
                temp = item['main']['temp']
                daily_forecasts[date_key]['temp_min'] = min(daily_forecasts[date_key]['temp_min'], temp)
                daily_forecasts[date_key]['temp_max'] = max(daily_forecasts[date_key]['temp_max'], temp)
            
            # Convert to list and sort by date
            daily_list = list(daily_forecasts.values())
            daily_list.sort(key=lambda x: x['date'])
            
            # Update UI for 5 days
            for i, day_data in enumerate(daily_list[:5], 1):
                if i in self.weather_labels:
                    labels = self.weather_labels[i]
                    
                    # Update day name
                    labels['day_name'].setText(day_data['day_name'])
                    
                    # Update weather description
                    labels['weather_desc'].setText(day_data['weather_desc'].title())
                    
                    # Update temperature
                    temp_min = int(day_data['temp_min'])
                    temp_max = int(day_data['temp_max'])
                    labels['temp'].setText(f"{temp_max}°C ← {temp_min}°C")
                    
                    # Update details
                    details_text = f"Precipitation: {day_data['pop']:.0f}%\nHumidity: {day_data['humidity']}%\nWind: {day_data['wind_speed']:.0f} km/h"
                    labels['details'].setText(details_text)
                    
                    # Update weather icon
                    icon_path = f"weather_icons/{day_data['weather_icon']}.png"
                    labels['icon_btn'].setIcon(QIcon(icon_path))
                    labels['icon_btn'].setIconSize(QSize(40, 40))
                    
        except Exception as e:
            print(f"Error updating forecast: {e}")

    def navigate_screen(self, stackWidget: QStackedWidget, index: int):
        stackWidget.setCurrentIndex(index)

    def load_user_info(self):
        self.txt_name.setText(self.user["name"])
        self.txt_email.setText(self.user["email"])
        self.txt_birthday.setDate(QDate.fromString(self.user["birthday"], "dd//MM//yyyy"))
        self.txt_gender.setCurrentText(self.user["gender"])
        self.btn_avatar.setIcon(QIcon(self.user["avatar"]))

    def update_avatar(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select Image","","Image Files(*.png *.jpg *jpeg *.bmp)")
        if file:
            self.user["avatar"] = file
            self.btn_avatar.setIcon(QIcon(file))
            update_user_avatar(self.id, file)

    def update_user_info(self):
        name = self.txt_name.text().strip()
        birthday = self.txt_birthday.date().toString("dd/MM/yyyy")
        gender = self.txt_gender.currentText()
        update_user(self.id, name, birthday, gender)
        msg.success_message("Update", "User info updated seccessfully")
        self.load_user_info()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    msg = Alert()
    login = Login()
    login.show()
    sys.exit(app.exec())        


    