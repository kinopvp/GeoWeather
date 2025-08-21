import requests
import sys
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

def display_banner():
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════╗
║              GeoWeather               ║
║   Location & Weather from your IP     ║
╚═══════════════════════════════════════╝{Style.RESET_ALL}
"""
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=10)
        return response.json().get("ip", "Unknown")
    except requests.RequestException:
        return "Unknown"

def geolocate_ip(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
        data = response.json()
        return {
            "city": data.get("city", "Unknown"),
            "region": data.get("region", "Unknown"),
            "country": data.get("country_name", "Unknown"),
            "lat": data.get("latitude"),
            "lon": data.get("longitude"),
            "timezone": data.get("timezone", "Unknown")
        }
    except requests.RequestException:
        return {"city": "Unknown", "region": "Unknown", "country": "Unknown", "lat": None, "lon": None, "timezone": "Unknown"}

def get_weather_data(lat, lon):
    """
    Get simplified weather data from wttr.in API.
    """
    if lat is None or lon is None:
        return "Weather information unavailable."
    
    try:
        # Get current weather in JSON format
        url = f"https://wttr.in/{lat},{lon}?format=j1"
        response = requests.get(url, timeout=15)
        data = response.json()
        
        current = data["current_condition"][0]
        weather_desc = current["weatherDesc"][0]["value"]
        temp_c = current["temp_C"]
        temp_f = current["temp_F"]
        humidity = current["humidity"]
        
        # Check if it's raining/snowing
        precipitation = ""
        if "rain" in weather_desc.lower() or "drizzle" in weather_desc.lower():
            precipitation = " 🌧️"
        elif "snow" in weather_desc.lower():
            precipitation = " ❄️"
        elif "cloud" in weather_desc.lower():
            precipitation = " ☁️"
        elif "sun" in weather_desc.lower() or "clear" in weather_desc.lower():
            precipitation = " ☀️"
        
        return f"Temperature: {temp_c}°C ({temp_f}°F)\nConditions: {weather_desc}{precipitation}\nHumidity: {humidity}%"
        
    except requests.RequestException:
        return "Weather service unavailable."
    except (KeyError, IndexError):
        return "Weather data format error."

def main():
    """Main function to run GeoWeather."""
    try:
        display_banner()
        
        # Get current local time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Step 1: Get public IP
        print(f"{Fore.YELLOW}🌍 Fetching your public IP...")
        ip = get_public_ip()
        print(f"{Fore.YELLOW}📍 Public IP: {Style.BRIGHT}{ip}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}🕐 Current Time: {current_time}")

        if ip == "Unknown":
            print(f"{Fore.RED}❌ Unable to fetch IP address. Check your internet connection.")
            return

        # Step 2: Get location from IP
        print(f"\n{Fore.GREEN}🔍 Getting location information...")
        location = geolocate_ip(ip)
        print(f"{Fore.GREEN}📍 Location: {Style.BRIGHT}{location['city']}, {location['region']}, {location['country']}{Style.RESET_ALL}")
        if location['timezone'] != "Unknown":
            print(f"{Fore.GREEN}🌐 Timezone: {location['timezone']}")

        # Step 3: Fetch and display simplified weather
        print(f"\n{Fore.CYAN}🌤️  Fetching weather information...")
        weather_info = get_weather_data(location["lat"], location["lon"])
        print(f"{Fore.CYAN}{weather_info}")
        
        print(f"\n{Fore.MAGENTA}✨ Done! Stay weather-aware! ✨{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}❌ Interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
