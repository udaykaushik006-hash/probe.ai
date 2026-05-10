import webbrowser
import pywhatkit

def run_command(command):

    if "open instagram" in command:
        webbrowser.open("https://instagram.com")
        return "Opening Instagram"

    if "open spotify" in command:
        webbrowser.open("https://open.spotify.com")
        return "Opening Spotify"

    if "play" in command:
        song = command.replace("play", "")
        pywhatkit.playonyt(song)
        return f"Playing {song}"

    if "open youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    if "open google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google"
    
    if "open snapchat" in command:
        webbrowser.open("http://snachat.com")
        return "Opening Snapchat"
    
    if "open twitter" in command:
        webbrowser.open("https://twitter.com")
        return "Opening Twitter" 
    
    if "open facebook" in command:
        webbrowser.open("https://facebook.com")
        return "Opening Facebook"
    
    if "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        return "Opening LinkedIn"
    
    if "open swift" in command:
        webbrowser.open("https://swift.com")
        return "Opening Swift"
    
    if "open wikipedia" in command:
        webbrowser.open("https://wikipedia.org")
        return "Opening Wikipedia"
    
    if "open github" in command:
        webbrowser.open("https://github.com")
        return "Opening GitHub"
    
    if "open reddit" in command:
        webbrowser.open("https://reddit.com")
        return "Opening Reddit"
    
    if "open netflix" in command:
        webbrowser.open("https://netflix.com")
        return "Opening Netflix"
    
    if "open amazon" in command:
        webbrowser.open("https://amazon.com")
        return "Opening Amazon"
    
    if "open ebay" in command:
        webbrowser.open("https://ebay.com")
        return "Opening eBay"
    
    if "open twitch" in command:
        webbrowser.open("https://twitch.tv")
        return "Opening Twitch"
    
    if "open discord" in command:
        webbrowser.open("https://discord.com")
        return "Opening Discord"
    
    if "open stocks" in command:
        webbrowser.open("https://finance.yahoo.com")
        return "Opening Stocks"
    
    if "open zomato" in command:
        webbrowser.open("https://zomato.com")
        return "Opening Zomato"
    
    if "open swiggi" in command:
        webbrowser.open("https://swiggi.com")
        return "Opening Swiggi"
    
    if "open uber" in command:
        webbrowser.open("https://uber.com")
        return "Opening Uber"
    
    if "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp"
    
    if "open chatgpt" in command:
        webbrowser.open("https://chat.openai.com")
        return "Opening ChatGPT"
    
    if "open gmail" in command:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail"
    
    if "open calendar" in command:
        webbrowser.open("https://calendar.google.com")
        return "Opening Calendar"
    
    if "open maps" in command:
        webbrowser.open("https://maps.google.com")
        return "Opening Maps"
    
    if "open drive" in command:
        webbrowser.open("https://drive.google.com")
        return "Opening Drive"
    
    if "open photos" in command:
        webbrowser.open("https://photos.google.com")
        return "Opening Photos"
    
    if "open news" in command:
        webbrowser.open("https://news.google.com")
        return "Opening News"
    
    if "open translate" in command:
        webbrowser.open("https://translate.google.com")
        return "Opening Translate"
    
    if "open docs" in command:
        webbrowser.open("https://docs.google.com")
        return "Opening Docs"
    
    if "open sheets" in command:
        webbrowser.open("https://sheets.google.com")
        return "Opening Sheets"
    
    if "open slides" in command:
        webbrowser.open("https://slides.google.com")
        return "Opening Slides"
    
    if "open gorky" in command:
        webbrowser.open("https://gorky.ai")
        return "Opening Gorky"
    
    if "open canva" in command:
        webbrowser.open("https://canva.com")
        return "Opening Canva"
    
    if "open figma" in command:
        webbrowser.open("https://figma.com")
        return "Opening Figma"
    
    if "open notion" in command:
        webbrowser.open("https://notion.so")
        return "Opening Notion"
    
    if "jiosaavn" in command:
        webbrowser.open("https://jiosaavn.com")
        return "Opening JioSaavn"
    
    if "open soundcloud" in command:
        webbrowser.open("https://soundcloud.com")
        return "Opening SoundCloud"
    
    if "open apple music" in command:
        webbrowser.open("https://music.apple.com")
        return "Opening Apple Music"
        
    if "open tinder" in command:
        webbrowser.open("https://tinder.com")
        return "Opening Tinder"
    
    if "open zoom" in command:
        webbrowser.open("https://zoom.us")
        return "Opening Zoom"
    
    if "hianime" in command:
        webbrowser.open("https://hianime.com")
        return "Opening HiAnime"
    
    if "open prime video" in command:
        webbrowser.open("https://primevideo.com")
        return "Opening Prime Video"
    
    if "open disney plus" in command:
        webbrowser.open("https://disneyplus.com")
        return "Opening Disney Plus"
    
    if "open jiohotstar" in command:
        webbrowser.open("https://jiohotstar.com")
        return "Opening JioHotstar"
    
    if "open sony liv" in command:
        webbrowser.open("https://sonyliv.com")
        return "Opening Sony Liv"
    
    if "open zee5" in command:
        webbrowser.open("https://zee5.com")
        return "Opening Zee5"
    
    if "open employment news" in command:
        webbrowser.open("https://timesofindia.indiatimes.com/jobs/employment-news")
        return "Opening Employment News"
        
    if "open indeed" in command:
        webbrowser.open("https://indeed.com")
        return "Opening Indeed"
    
    if "open daily news nearme" in command:
        webbrowser.open("https://news.google.com/nearme")
        return "Opening Daily News"
    
    if "open weather" in command:
        webbrowser.open("https://weather.google.com")
        return "Opening Weather"
    
    if "open camera" in command:
        webbrowser.open("https://webcammictest.com")
        return "Opening Camera"
    
    if "open calculator" in command:
        webbrowser.open("https://www.calculator.com")
        return "Opening Calculator"
    
    if "open calendar" in command:
        webbrowser.open("https://calendar.google.com")
        return "Opening Calendar"
    
    if "open chat gpt" in command:
        webbrowser.open("https://chat.openai.com")
        return "Opening ChatGPT"
        "n\nYou can also ask me to play music, search the web, or answer questions!"
    
    if "open deep seek" in command:
        webbrowser.open("https://deepseek.com")
        return "Opening DeepSeek"
    
    if "open deepsearch" in command:
        webbrowser.open("https://deepsearch.ai")
        return "Opening DeepSearch"
    

    
    return None