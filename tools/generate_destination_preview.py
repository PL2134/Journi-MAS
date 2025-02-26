from typing import Any, Optional
from smolagents.tools import Tool
import random

class GenerateDestinationPreviewTool(Tool):
    name = "generate_destination_preview"
    description = "Generates a vivid textual description of a travel destination's scenery and atmosphere."
    inputs = {'destination': {'type': 'string', 'description': 'The travel destination to describe (e.g., "Paris", "Tokyo", "Bali").'}}
    output_type = "string"

    def __init__(self):
        super().__init__()
        
        # List of times of day and weather for variety
        self.atmospheres = [
            "at sunrise with golden light washing over the landscape",
            "during blue hour twilight when the sky turns a deep azure",
            "on a clear day with vibrant colors and perfect visibility",
            "at sunset with dramatic golden and pink hues in the sky",
            "in the evening with twinkling lights creating a magical atmosphere",
            "on a misty morning with an ethereal quality to the scenery",
            "under dramatic storm clouds creating contrast and mood",
            "during cherry blossom season with delicate pink flowers everywhere",
            "in autumn with rich red and gold foliage creating a warm palette",
            "after a light rain when everything looks fresh and vibrant"
        ]
        
        # Common descriptions for popular destinations
        self.destination_descriptions = {
            "paris": "The elegant Haussmannian buildings line wide boulevards as the Eiffel Tower rises above the city. Charming cafés spill onto cobblestone streets where locals and visitors sip espresso at tiny tables. The Seine River winds through the heart of the city, with historic bridges connecting the Left and Right Banks. In the distance, the white domes of Sacré-Cœur Basilica crown the artistic Montmartre neighborhood.",
            
            "tokyo": "Neon signs and digital screens create a kaleidoscope of colors in bustling Shibuya as modern skyscrapers tower above ancient temples and shrines. In Shinjuku, business districts blend with entertainment areas filled with restaurants and izakayas hidden in narrow alleys. Cherry blossoms or manicured autumn maples add seasonal beauty to parks like Ueno and Yoyogi. The iconic Tokyo Tower or Tokyo Skytree punctuate the sprawling skyline of this massive metropolis.",
            
            "new york": "The iconic Manhattan skyline rises dramatically with the Empire State Building, One World Trade Center, and other distinctive towers creating a jagged silhouette against the sky. Yellow taxis navigate the grid-like streets as diverse neighborhoods each showcase unique character. Central Park provides a vast green oasis amid the urban landscape, with paths winding past meadows, ponds, and rocky outcrops. The Brooklyn Bridge spans the East River, its gothic arches and suspension cables creating a classic view of the city.",
            
            "rome": "Ancient ruins of the Colosseum and Roman Forum stand as reminders of a glorious imperial past, their weathered stone glowing warm amber in the Mediterranean sun. Renaissance fountains splash in baroque piazzas where locals and tourists gather to socialize and enjoy gelato. Narrow cobblestone streets wind through historic neighborhoods, opening suddenly onto magnificent churches with ornate facades. The Tiber River flows beneath historic bridges, while domes and bell towers punctuate the skyline of this eternal city.",
            
            "bali": "Lush terraced rice fields cascade down hillsides in vivid shades of green, their curved lines following the natural contours of the land. Palm trees sway above pristine beaches where turquoise waters meet white or black volcanic sand. Stone temples with intricate carvings are adorned with colorful offerings and yellow parasols. In the interior, volcanic mountains rise dramatically above tropical forests and river valleys, with the conical peak of Mount Agung dominating the landscape.",
            
            "london": "The historic Tower Bridge spans the Thames River with its distinctive blue suspension structure and Victorian Gothic towers. Along the embankment, the Houses of Parliament and Big Ben create an instantly recognizable silhouette. Royal parks offer vast green spaces amid the bustling city, with perfectly manicured gardens and serene lakes. Historic buildings sit alongside modern architectural marvels like The Shard and The Gherkin, creating a skyline that blends centuries of history with contemporary innovation.",
            
            "sydney": "The Opera House's distinctive sail-shaped roofs curve gracefully against the deep blue of Sydney Harbour. The massive steel arch of the Harbour Bridge frames the city skyline of gleaming skyscrapers. Ferries crisscross the sparkling waters as golden beaches like Bondi and Manly offer perfect crescents of sand against the Pacific Ocean. Native flora adds splashes of unique color and texture throughout the city's gardens and surrounding national parks.",
            
            "mount fuji": "The perfectly symmetrical volcanic cone rises majestically from the surrounding plain, its snow-capped peak often visible for miles around. In spring, cherry blossoms create pink frames for the mountain at viewing points around the Five Lakes region. Autumn brings rich red maple leaves that contrast with the blue lakes reflecting Fuji's imposing silhouette. Forests of pine and cypress cover the lower slopes, transitioning to barren volcanic rock higher up the mountain. At dawn, the peak often catches the first rays of sun in a phenomenon known as 'red Fuji.'",
            
            "santorini": "Whitewashed cubic buildings with blue domed churches cascade down steep volcanic cliffs that plunge dramatically into the deep blue Aegean Sea. Narrow winding pathways connect the buildings, occasionally opening to reveal breathtaking panoramic views of the caldera. The stark white architecture creates a striking contrast against the black and red volcanic rocks and the multi-hued blues of the sky and sea. At sunset, the entire landscape transforms with a golden glow that gradually shifts to pink and purple hues reflecting off the white buildings.",
            
            "kyoto": "Ancient wooden temples and shrines with distinctive curved roofs are nestled among Japanese maple trees and meticulously maintained Zen gardens. Stone pathways lead through bamboo groves that filter sunlight into ethereal green patterns. Geisha in colorful kimonos occasionally appear on traditional streets lined with machiya wooden houses. The Kamo River flows gently through the city with mountains forming a protective embrace around this cultural heartland. In spring, cherry blossoms create canopies of pink, while autumn brings a spectacular display of red, orange, and gold foliage."
        }

    def forward(self, destination: str) -> str:
        # Select a random atmosphere for variety
        atmosphere = random.choice(self.atmospheres)
        
        # Normalize destination name
        dest_lower = destination.lower()
        
        # Look for matching or partial matching descriptions
        description = None
        for key, value in self.destination_descriptions.items():
            if key in dest_lower or dest_lower in key:
                description = value
                break
        
        # Generate a detailed description if no specific one is found
        if not description:
            # Make the generation deterministic based on destination name
            random.seed(sum(ord(c) for c in destination))
            
            # Generate elements based on destination name characteristics
            geography_types = [
                "coastal region with dramatic cliffs and pristine beaches",
                "mountainous landscape with snow-capped peaks and alpine meadows",
                "historic city with ancient architecture and cultural landmarks",
                "tropical paradise with lush vegetation and crystal-clear waters",
                "desert landscape with striking rock formations and endless horizons",
                "rural countryside with rolling hills and picturesque villages",
                "island archipelago with white sand beaches and swaying palm trees",
                "urban metropolis with impressive skyline and bustling streets",
                "forested wilderness with pristine lakes and abundant wildlife",
                "volcanic terrain with otherworldly landscapes and geothermal features"
            ]
            
            natural_features = [
                "serene lakes reflecting the surrounding scenery",
                "winding rivers cutting through the landscape",
                "lush gardens showcasing local plant species",
                "dramatic waterfalls cascading down rocky cliffs",
                "ancient forests with towering trees",
                "colorful wildflower meadows stretching to the horizon",
                "unique rock formations sculpted by wind and water",
                "coral reefs teeming with vibrant marine life",
                "majestic canyons revealing geological history",
                "natural hot springs steaming in the landscape"
            ]
            
            human_elements = [
                "historic architecture that tells stories of the past",
                "charming local markets filled with authentic goods",
                "traditional villages preserving cultural heritage",
                "impressive religious structures adorned with intricate details",
                "modern architectural marvels blending with the environment",
                "inviting cafés and restaurants showcasing local cuisine",
                "artisan workshops keeping traditional crafts alive",
                "carefully preserved archaeological sites",
                "botanical gardens displaying plant diversity",
                "scenic viewpoints offering panoramic vistas"
            ]
            
            geography = random.choice(geography_types)
            feature = random.choice(natural_features)
            element = random.choice(human_elements)
            
            description = f"{destination} is a breathtaking {geography}. Visitors are drawn to its {feature} that create unforgettable vistas at every turn. The area is also known for its {element}, making it a perfect destination for travelers seeking both natural beauty and cultural experiences. The unique atmosphere and character of {destination} create an unforgettable travel experience that captivates visitors from around the world."
        
        # Format the final response
        return f"✨ Scenic Description: {destination} ✨\n\n{description}\n\nImagine experiencing {destination} {atmosphere} - this is when the destination truly reveals its magic to visitors."
