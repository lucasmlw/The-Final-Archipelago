def get_absolute_coordinates_from_mouse_click(mouse_x, mouse_y, camera_x, camera_y):
    return mouse_x + camera_x, mouse_y + camera_y
    
def should_be_rendered(obj_x, obj_y, camera_x, camera_y):
    return (obj_x >= camera_x) and (obj_y >= camera_y)

def get_image_sources(url, use_class = False):
    try:
        headers={'User-Agent': 'Mozilla/5.0'}
        # Send an HTTP request to get the HTML page
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            img_tags = None
            if use_class:
                # Find all <div> tags in the HTML with class monster icon
                img_tags = soup.find('div', class_='monster-icon')
            else:
                # Find all <img> tags in the HTML
                img_tags = soup.find_all('img')
            
            if img_tags == None:
                return None
                
            if use_class:
                if img_tags == None:
                    return None
                else:
                    try:
                        src = img_tags.find('a').get('href')
                        
                        if src:
                            return src
                        else:
                            return None
                    except Exception as e:
                        return None
            else:
                # Print the src attribute of each <img> tag
                for img_tag in img_tags:
                    src = img_tag.get('src')
                    if src:
                        return src
                    else:
                        print("No src attribute found for an image tag.")
                        return None
            
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
        
def load_image_from_url(url):
    try:
        # Send an HTTP request to get the image
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Load the image using Pygame
            image_data = BytesIO(response.content)
            image = pygame.image.load(image_data)
            
            return image
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
        
def get_dnd_image():
    monster_name = random_monster_name()
    print(monster_name)
    
    master_url = 'https://www.aidedd.org/dnd/monstres.php?vo=' + monster_name # Only 300 monsters
    image_url = get_image_sources(master_url)
    monster_image = None
    if image_url != None:
        monster_image = load_image_from_url(image_url)
        return monster_image
    master_url = 'https://www.dndbeyond.com/monsters?filter-search=' + monster_name.replace('-', ' ') # Lots of monsters
    image_url = get_image_sources(master_url, True)
    if image_url != None:
        monster_image = load_image_from_url(image_url)
        return monster_image
    return None
    
## use pandas to read in the excel file and choose a random monster
pd.set_option('display.max_columns', None)
df = pd.read_excel('Monster Spreadsheet (D&D5e).xlsx') # 800 monsters

def random_monster():
    selection = random.choice(list(df["Name"]))
    return df.loc[df['Name'] == selection]

def random_monster_name():
    selection = random.choice(list(df["Name"]))
    un_processed_name = df.loc[df['Name'] == selection]['Name'].tolist()[0]
    #un_processed_name = 'Chain Devil'
    if 'NPC' in un_processed_name or 'Beasts' in un_processed_name or 'Monsters' in un_processed_name or 'Misc' in un_processed_name or 'Creature' in un_processed_name or 'Genie' in un_processed_name or 'Lycanthrope' in un_processed_name:
        un_processed_name = un_processed_name.replace('NPC', '').replace('Monsters', '').replace('Beasts', '').replace('Misc', '').replace('Creature', '').replace('Genie', '').replace('Lycanthrope', '').replace(',', '').replace('.', '').lstrip().replace(' ', '-').lower()
    else:
        if un_processed_name.startswith("Demon") or un_processed_name.startswith("Devil") or un_processed_name.startswith("Dinosaur"):
            un_processed_name = un_processed_name.replace('Demon', '').replace('Devil', '').replace('Dinosaur', '').replace(',', '').replace('.', '').lstrip().replace(' ', '-').lower()
        else:
            un_processed_name = un_processed_name.lower().replace(',', '').replace(' ', '-').replace('.', '')
    return un_processed_name
    
if __name__ == "__main__":
    get_image_sources('https://www.dndbeyond.com/monsters?filter-search=raven', True)
    print(type(get_dnd_image()))
    print(random_monster()['Name'])
    print("wait")
    print(random_monster_name())
    
    # Width, Height, Frame rate, Camera Speed
    #game = DndMainGame(width, height-60, 60, 5) 
    #game.main()
