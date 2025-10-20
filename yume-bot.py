import discord, time, random, pickle, pathlib
from discord.ext.commands import Bot
from discord.ext.commands.core import command
import requests
import cv2, os, threading


alphabet_spécial = ["զ", "է", "ր", "ը", "ֆ", "կ", "լ", "մ", "Ր", "Խ", "Մ", "Ւ", "Գ", "Բ", "Պ", "Վ", "q", "Ը", "Տ", "խ",
 "ա", "տ", "բ", "բ", "Ֆ", "ը"]

taille_maximale_fichier = 500000

def mot_aléatoire():
    mot_final = ""
    for i in range(7):
        lettre_aléatoire = alphabet_spécial[random.randint(0,25)]
        mot_final += lettre_aléatoire  
    return mot_final 

def dernierIndiceMaximum(liste):
    maxi = liste[0]
    longueur=len(liste)
    indice_max = 0
    for i in range(longueur):
        if liste[i] >= maxi:
            maxi = liste[i]
            indice_max = i
    return indice_max

def error_message(text):
    embed=discord.Embed()
    embed.add_field(name="❌  Echec de la commande...", value=text, inline=False)
    return embed

# Récupération du token (à remplacer par vos propres données)
with open("token.txt", "r") as fichier:
    token = fichier.read()

# Commandes basiques
client = discord.Client()

@client.event
async def on_ready():
    print("le bot est prêt !")
    # ID du canal modifié
    channel = client.get_channel(123456789012345678)
    with open("data/statut.txt", "r") as fichier:
        statut = fichier.read()
    await client.change_presence(activity=discord.Game(name=statut))

@client.event
async def on_message(message):
    contenu = message.content
    list_roles = []
    try:
        contenu = int(contenu)
        msg = contenu + 1
        for roles in message.author.roles:
                roles = str(roles)
                list_roles.append(roles)

        if not "bot c" in list_roles and not "bot" in list_roles :
            with open("data/mode_count.txt", "r") as fichier:
                mode = fichier.read()
                print(mode)
                if mode == "True":
                    await message.channel.send(msg)
    except ValueError:
        pass

    if message.content.startswith(".help"):
        embed=discord.Embed()
        embed=discord.Embed(color=0x0008ff)
        embed.set_thumbnail(url="https://example.com/bot_icon.jpg")  # URL modifiée
        embed.add_field(name=" 📃 Voici la liste des commandes disponibles : ", value="-------------------------------", inline=False)
        embed.add_field(name="1️⃣ .del [nombre]", value="supprime un nombre de message", inline=True)
        embed.add_field(name="2️⃣ .[nom]", value="Envoie une photo de [nom] au hasard", inline=True)
        embed.add_field(name="3️⃣ .changestatut [nouveau statut]", value="Change le statut du bot                                       ", inline=True)
        embed.add_field(name="4️⃣ .add [nom]", value="Ajoute une image de [nom] à la collection", inline=True)
        embed.add_field(name="5️⃣ .stop", value="stoppe le programme. A FAIRE SEULEMENT EN CAS D'URGENCE", inline=True)
        embed.add_field(name="6️⃣ .add_svp [nom]", value="Proposez votre nouvelle catégorie d'images.", inline=True)
        embed.add_field(name="7️⃣ .show [nom]", value="Affiche toutes les images de [nom]", inline=True)
        embed.add_field(name="8️⃣ .mode_count True/False", value="Active le mode comptage.", inline=True)
        await message.channel.send(embed=embed)

    if message.content.startswith(".toplist"):
        with open(f"data/categories.txt", "r") as fichier:
            catégories = fichier.read().splitlines()
            dico = {}
            liste_croissant = []
            for name in catégories:
                with open(f"data/{name}_pictures.txt", "r") as fichier2:
                    taille = len(fichier2.read().splitlines())
                dico[taille] = name
            index_précédent = 0
            for index in dico:
                liste_croissant.append(index)
            liste_croissant.sort()
            print(liste_croissant)
            for i in range(len(liste_croissant)-5):
                liste_croissant.pop(0)
            embed=discord.Embed(title="Classement des catégories ")
            embed.add_field(name=f"🥇{dico[liste_croissant[4]]}", value=f"avec {liste_croissant[4]} images !", inline=False)
            embed.add_field(name=f"🥈{dico[liste_croissant[3]]}", value=f"avec {liste_croissant[3]} images !", inline=False)
            embed.add_field(name=f"🥉{dico[liste_croissant[2]]}", value=f"avec {liste_croissant[2]} images !", inline=False)
            embed.add_field(name=f"4️⃣ {dico[liste_croissant[1]]}", value=f"avec {liste_croissant[1]} images !", inline=False)
            embed.add_field(name=f"5️⃣ {dico[liste_croissant[0]]}", value=f"avec {liste_croissant[0]} images !", inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith(".del"):
        contenu = message.content
        list_roles = []
        for roles in message.author.roles:
            roles = str(roles)
            list_roles.append(roles)

        if not "bot c" in list_roles and not "bot" in list_roles :
            if message.author.guild_permissions.administrator == True:
                print(message.author.guild_permissions.administrator)
                try:
                    number = int(message.content.split()[1])
                    messages = await message.channel.history(limit = number + 1).flatten()

                    for eachmessage in messages:
                        await eachmessage.delete()

                    #Message reussie
                    embed=discord.Embed()
                    embed.add_field(name=f"✅  {number} Messages ont étés supprimés !", value="Bravo !", inline=False)
                    await message.channel.send(embed=embed)

                    time.sleep(5)
                    messages = await message.channel.history(limit = 1).flatten()

                    for eachmessage in messages:
                        await eachmessage.delete()

                except IndexError:
                    #error message
                    embed = error_message("Veuillez préciser le nombre de message à supprimer.")
                    await message.channel.send(embed=embed)
                except ValueError:
                    #error message
                    embed=discord.Embed()
                    embed.add_field(name="❌  Echec de la commande...", value="Veuillez donner un numéro après le del et mettre un espace.", inline=False)
                    await message.channel.send(embed=embed)

            if message.author.guild_permissions.administrator == False:
                #error message
                embed=discord.Embed()
                embed.add_field(name="❌  Echec de la commande...", value="Cette commande nécéssite la permission administrateur.", inline=False)
                await message.channel.send(embed=embed)

    if message.content.startswith(".changestatut"):
        if message.author.guild_permissions.administrator == True and message.author.id == 123456789012345678:  # ID modifié
            try:
                statut = message.content
                statut = statut.replace(".changestatut ", "")
                with open("data/statut.txt", "w") as fichier:
                    fichier.write("")
                    fichier.write(statut)
                await client.change_presence(activity=discord.Game(name=statut))
                #message reussie
                embed=discord.Embed()
                embed.add_field(name="✅ Commande réussie", value=f'Le statut a été remplacé par "{statut}"', inline=False)
                await message.channel.send(embed=embed)
            except IndexError:
                #error
                embed=discord.Embed()
                embed.add_field(name="❌  Echec de la commande...", value="Veuillez préciser le nouveau statut.", inline=False)
                await message.channel.send(embed=embed)
        else:
            #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="Cette commande nécéssite la permission administrateur.", inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith("."):
        # ID du canal modifié
        if message.channel.id != 123456789012345678:
            command = message.content
            command = command.replace(".", "")
            with open(f"data/categories.txt", "r") as fichier:
                catégories = fichier.read();catégories = catégories.splitlines()
            if command in catégories:
                command = command.lower()
                print(command)
                with open(f"data/{command}_pictures.txt", "r") as fichier:
                    pictures = fichier.read()
                    pictures = pictures.splitlines()
                random_picture = pictures[random.randint(0, (len(pictures)-1))]
                await message.channel.send(random_picture)

    if message.content.startswith(".size"):
        if message.author.guild_permissions.administrator == True:
            command = ((message.content).replace(".size", "")).split()
            if len(command) == 1:
                nom = (command[0]).lower()
                with open(f"data/categories.txt", "r") as fichier:
                            catégories = fichier.read();catégories = catégories.splitlines()
                if nom in catégories:
                    file_size = pathlib.Path(rf'data/{nom}_pictures.txt').stat().st_size
                    with open(f"data/{nom}_pictures.txt", "r") as fichier:
                        pictures = fichier.read();pictures = pictures.splitlines()
                    taille_restante = int((taille_maximale_fichier - file_size)/1000)
                    nombres_de_lignes = len(pictures)
                    embed=discord.Embed()
                    embed.add_field(name="✅ Commande réussie !", value=f"La catégorie {nom} contient {nombres_de_lignes} images. Il reste {taille_restante}Ko.", inline=False)
                    await message.channel.send(embed=embed)
                else:
                    #error message
                    embed=discord.Embed()
                    embed.add_field(name="❌  Echec de la commande...", value="Cette catégorie d'image n'existe pas", inline=False)
                    await message.channel.send(embed=embed)
            else:
                #error message
                embed=discord.Embed()
                embed.add_field(name="❌  Echec de la commande...", value="Veuillez écire la comande comme ceci : .size [nom]", inline=False)
                await message.channel.send(embed=embed)
        else:
            #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="Cette commande nécéssite la permission administrateur.", inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith(".add"):
        if not message.content.startswith(".add_categorie"):
            if not message.content.startswith(".add_svp"):
                # IDs modifiés
                if message.author.guild_permissions.administrator == True or message.author.id == 123456789012345678 or message.author.id == 123456789012345679 or message.author.id == 123456789012345680 or message.author.id == 123456789012345681:
                    command = message.content
                    command = command.replace(".add", "")
                    command = command.split()
                    if len(command) == 2:
                        nom = command[0]
                        nom = nom.lower()
                        lien = command[1]
                        with open(f"data/categories.txt", "r") as fichier:
                            catégories = fichier.read();catégories = catégories.splitlines()
                        if nom in catégories:
                            if "https://cdn.discordapp.com/attachments/" in lien or "https://media.discordapp.net/attachments" in lien:
                                file_size = pathlib.Path(rf'data/{nom}_pictures.txt').stat().st_size
                                print(file_size)
                                if file_size < taille_maximale_fichier:
                                    with open(f"data/{nom}_pictures.txt", "r") as fichier:
                                        content = fichier.read()
                                        if content == "":
                                            saut_de_ligne = ""
                                        else:
                                            saut_de_ligne = "\n"
                                    with open(f"data/{nom}_pictures.txt", "a") as fichier:
                                        fichier.write(saut_de_ligne + lien)
                                    embed=discord.Embed()
                                    embed.set_thumbnail(url=lien)
                                    #partie lol
                                    note = random.randint(0,20)
                                    if note > 19:
                                        text = "Perfect !"
                                    elif note > 15:
                                        text = "Stylééé"
                                    elif note > 10:
                                        text = "Pas mal !"
                                    elif note > 5:
                                        text = "Bof.. Même fanny est plus stylée.."
                                    elif note > 0:
                                        text = "Mais qu'est-ce qui t'as pris de mettre une image aussi nulle ??"
                                    elif note == 0:
                                        text = "... Grosse merde.."

                                    #_____________
                                    embed.add_field(name="✅ Commande réussie", value=f"L'image a été ajoutée à la collection {nom}.", inline=False)
                                    embed.add_field(name=f"Note de l'image : {note}/20", value=text, inline=False)
                                    await message.channel.send(embed=embed)
                                    #_____________
                                    with open(f"data/{name}_pictures.txt", "r") as fichier:
                                        pictures = fichier.read()
                                        pictures = pictures.splitlines()
                                    nombre_images = len(pictures)
                                    if nombre_images == 1000:
                                        with open(f"data/{name}_pictures.txt", "w") as fichier:
                                            fichier.write(message.author.mention + "1" )
                                else:
                                    #error message
                                    embed=discord.Embed()
                                    embed.add_field(name="❌  Echec de la commande...", value="Le fichier est plein !", inline=False)
                                    await message.channel.send(embed=embed)
                            else:
                                #error message
                                embed=discord.Embed()
                                embed.add_field(name="❌  Echec de la commande...", value="Le lien doit commencer par https://cdn.discordapp.com/attachments/ ou  https://media.discordapp.net/attachments.", inline=False)
                                await message.channel.send(embed=embed)
                        else:
                            #error message
                            embed=discord.Embed()
                            embed.add_field(name="❌  Echec de la commande...", value="Cette catégorie d'image n'existe pas", inline=False)
                            await message.channel.send(embed=embed)
                    else:
                        #error message
                        embed=discord.Embed()
                        embed.add_field(name="❌  Echec de la commande...", value="Veuillez écire la comande comme ceci : .add [nom] [lien]", inline=False)
                        await message.channel.send(embed=embed)
                else:
                    #error message
                    embed=discord.Embed()
                    embed.add_field(name="❌  Echec de la commande...", value="Cette commande nécéssite la permission administrateur.", inline=False)
                    await message.channel.send(embed=embed)

    if message.content.startswith(".show"):
        if message.author.guild_permissions.administrator == True:
            command = message.content
            command = command.replace(".show", "")
            command = command.lower()
            command = command.split()
            if len(command) == 1:
                with open(f"data/categories.txt", "r") as fichier:
                    catégories = fichier.read();catégories = catégories.splitlines()
                if command[0] in catégories:
                    name = command[0]
                    with open(f"data/{name}_pictures.txt", "r") as fichier:
                        pictures = fichier.read()
                        pictures = pictures.splitlines()
                    number = 1
                    for link in pictures:
                        await message.channel.send(str(number) + " " + link)
                        number += 1
                else:
                    #error message
                    embed=discord.Embed()
                    embed.add_field(name="❌  Echec de la commande...", value="Cette catégorie d'image n'existe pas", inline=False)
                    await message.channel.send(embed=embed)
            else:
                #error message
                embed=discord.Embed()
                embed.add_field(name="❌  Echec de la commande...", value="Veuillez écire la comande comme ceci : .show [name]", inline=False)
                await message.channel.send(embed=embed)
        else:
            #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="Cette commande nécéssite la permission administrateur.", inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith(".add_svp"):
        command = message.content
        command = command.replace(".add_svp ", "")
        name = command
        if len(name) < 25:
            try:
                with open(f"data/add_svp.txt", "a") as fichier:
                        fichier.write("\n" + command)
                embed=discord.Embed()
                embed.add_field(name="✅ Commande réussie", value=f"Des images de {name} seront peut être ajoutées.", inline=False)
                await message.channel.send(embed=embed)
            except UnicodeEncodeError:
                embed=discord.Embed()
                embed.add_field(name="❌  Echec de la commande...", value="Cette police ne fonctionne pas.", inline=False)
                await message.channel.send(embed=embed)
        else:
            #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="Ce nom est trop grand !", inline=False)
            await message.channel.send(embed=embed)
       
    if message.content.startswith(".stop"):
        if message.author.guild_permissions.administrator == True:
            #error message
            embed=discord.Embed()
            embed.add_field(name="⚠️ Fermeture du bot en urgence.", value="Veuillez vous addresser à l'administrateur pour le redémarrer", inline=False)
            await message.channel.send(embed=embed)
            exit()
        else:
            #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="Cette commande nécéssite la permission administrateur.", inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith(".mode_count"):
        if message.author.guild_permissions.administrator == True:
            command = message.content
            command = command.replace(".mode_count ", "")
            if command == "True":
                embed=discord.Embed()
                embed.add_field(name="✅ Commande réussie", value="Le mode comptage est mis sur True.", inline=False)
                await message.channel.send(embed=embed)
                with open("data/mode_count.txt", "w") as fichier:
                    fichier.write("True")
            elif command == "False":
                embed=discord.Embed()
                embed.add_field(name="✅ Commande réussie", value="Le mode comptage est mis sur False.", inline=False)
                await message.channel.send(embed=embed)
                with open("data/mode_count.txt", "w") as fichier:
                    fichier.write("False")
            else:
                #error message
                embed=discord.Embed()
                embed.add_field(name="❌  Echec de la commande...", value="Veuillez rédiger la commande comme ceci : .mode_count True/False", inline=False)
                await message.channel.send(embed=embed)
        else:
            #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="Cette commande nécéssite la permission administrateur.", inline=False)
            await message.channel.send(embed=embed)
 
    if message.content.startswith(".supp"):
        if message.author.guild_permissions.administrator == True:
            print(".supp")
            command = message.content
            command = command.replace(".supp", "")
            command = command.split()
            if len(command) == 2:
                name = command[0]
                number = command[1]
                with open(f"data/categories.txt", "r") as fichier:
                    catégories = fichier.read();catégories = catégories.splitlines()
                if name in catégories:
                    with open(f"data/{name}_pictures.txt", "r") as fichier:
                        images = fichier.read()
                        images = images.splitlines()    
                    try:
                        number = int(number)
                        if number > 0 and number <= len(images):
                            n = 1
                            numéro = number
                            numéro -= 1
                            with open(f"data/{name}_pictures.txt", "r") as fichier:
                                images = fichier.read()
                                images = images.splitlines()
                            lien_supp = images[numéro]
                            images.pop(numéro)
                            with open(f"data/{name}_pictures.txt", "w") as fichier:
                                fichier.write("")
                            for image in images:
                                if n == 1:
                                    a_la_ligne = ""
                                else:
                                    a_la_ligne = "\n"
                                with open(f"data/{name}_pictures.txt", "a") as fichier:
                                    n = 2
                                    fichier.write(a_la_ligne + image)
                            embed=discord.Embed()
                            embed.set_thumbnail(url=lien_supp)
                            embed.add_field(name="✅ Commande réussie", value="L'image a été supprimée.", inline=False)
                            await message.channel.send(embed=embed)        
                        else:
                            #error message
                            embed=discord.Embed()
                            embed.add_field(name="❌  Echec de la commande...", value="Ce numéro n'existe pas.", inline=False)
                            await message.channel.send(embed=embed)
                    except ValueError:
                        #error message
                            embed=discord.Embed()
                            embed.add_field(name="❌  Echec de la commande...", value="Veuillez entrer le numéro de l'image", inline=False)
                            await message.channel.send(embed=embed)
                else:
                #error message
                    embed=discord.Embed()
                    embed.add_field(name="❌  Echec de la commande...", value="Cette catégorie n'existe pas !", inline=False)
                    await message.channel.send(embed=embed)
            else:
                #error message
                embed=discord.Embed()
                embed.add_field(name="❌  Echec de la commande...", value="Veuillez rédiger la commande comme ceci : .supp [nom] [numero (1 = première image ajoutée)]", inline=False)
                await message.channel.send(embed=embed)
        else:
            #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="Cette commande nécéssite la permission administrateur.", inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith(".add_categorie"):
        # ID modifié
        if message.author.id == 123456789012345678:
            command = message.content
            command = command.replace(".add_categorie ", "")
            command = command.lower()
            with open(f"data/{command}_pictures.txt", "w") as fichier:
                fichier.write("")

            #écrit dans la liste des fichiers
            with open("data/categories.txt", "a") as fichier:
                fichier.write("\n" + command)

            embed=discord.Embed()
            embed.add_field(name="✅ Commande réussie", value=f"La catégorie {command} a été ajoutée !", inline=False)
            await message.channel.send(embed=embed)   
        else:
             #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="L'administrateur seulement peut exécuter cette commande.", inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith(".note"):
        command = message.content; command = command.replace(".note ", "")
        lien = command
        print(command)
        note = random.randint(0, 20)
        if "https://cdn.discordapp.com/attachments/" in lien or "https://media.discordapp.net/attachments" in lien:
            note = random.randint(0,20)
            if note > 19:
                text = "Perfect !"
            elif note > 15:
                text = "Pas mal du tout !"
            elif note > 10:
                text = "Mouais pas mal."
            elif note > 5:
                text = "Bof.. C'est un peu de la merde quoi.."
            elif note > 0:
                text = "C'est giga éclaté là."
            elif note == 0:
                text = "C'est vraiment de la grosse merde.."

            embed=discord.Embed()
            embed.set_thumbnail(url=lien)
            embed.add_field(name=f"Note de l'image : {note}/20", value=text, inline=False)
            await message.channel.send(embed=embed)
        else:
            #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="La commande doit s'écrire .note [lien]. Le lien doit commencer par https://cdn.discordapp.com/attachments/ ou  https://media.discordapp.net/attachments.", inline=False)
            await message.channel.send(embed=embed)

        if message.author.guild_permissions.administrator == True:
            command  = message.content;command = command.replace(".chernobyl ", "")
        else:
            #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="Cette commande nécéssite la permission administrateur.", inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith(".choisir"):
        command = message.content;command = command.replace(".choisir", "")
        if command != "":
            command = command.split()
            try:
                chiffre1 = int(command[0])
                chiffre2 = int(command[1])
                nombre_aléa = random.randint(chiffre1, chiffre2)
                embed=discord.Embed()
                embed.add_field(name=f"✅ Le chiffre est {nombre_aléa} !", value=f"Bravo ! (ou pas, je sais pas enfait)", inline=False)
                await message.channel.send(embed=embed)
            except ValueError:
                nombre_aléa = random.randint(0, (len(command) - 1))
                option = command[nombre_aléa]
                embed=discord.Embed()
                embed.add_field(name=f"✅ L'option choisie est {option} !", value=f"Bravo ! (ou pas, je sais pas enfait)", inline=False)
                await message.channel.send(embed=embed)
        else:
            #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="Veuillez écrire la commande comme ceci : .choisir [chiffre1/option1] [chiffre2/option2] (vous pouvez mettre une infinité d'options)", inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith(".recognize"):
        if not "cat" in message.content:
            command = message.content
            command = command.replace(".recognize ", "")
            command = command.split()
            if len(command) == 1:
                lien = command[0]
                if "https://cdn.discordapp.com/attachments/" in lien or "https://media.discordapp.net/attachments" in lien:
                    url = lien
                    response = requests.get(url)
                    with open("data/facial/image.jpg", "wb") as file:
                        file.write(response.content)

                    imagePath = "data/facial/image.jpg"

                    cascadeClassifierPath = "chemin/vers/haarcascade_frontalface_alt.xml"  # Chemin modifié

                    cascadeClassifier = cv2.CascadeClassifier(cascadeClassifierPath)

                    image = cv2.imread(imagePath)

                    grayImage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

                    detectedFaces = cascadeClassifier.detectMultiScale(grayImage, scaleFactor = 1.1, minNeighbors= 10)
                    
                    detect = False
                    for(x,y,width,height) in detectedFaces:
                        cv2.rectangle(image, (x,y), (x + width, y + height), (0,255,0),5)
                        detect = True

                    cv2.imwrite('data/facial/resultat.jpg',image)

                    if detect:
                        await message.channel.send("Visage détecté !")
                        await message.channel.send(file=discord.File('data/facial/resultat.jpg'))
                    else:
                        await message.channel.send(":x:Pas de visage détecté !")

                    os.remove('data/facial/resultat.jpg')
                    os.remove('data/facial/image.jpg')
                else:
                    #error me
                    embed=discord.Embed()
                    embed.add_field(name="❌  Echec de la commande...", value="Le lien doit commencer par https://cdn.discordapp.com/attachments/ ou  https://media.discordapp.net/attachments.", inline=False)
                    await message.channel.send(embed=embed)
            else:
                #error message
                embed=discord.Embed()
                embed.add_field(name="❌  Echec de la commande...", value="Veuillez rédiger la commande comme ceci : .recognize [lien]", inline=False)
                await message.channel.send(embed=embed)

    if message.content.startswith(".recognize_cat"):
        command = message.content
        command = command.replace(".recognize_cat ", "")
        command = command.split()
        if len(command) == 1:
            lien = command[0]
            if "https://cdn.discordapp.com/attachments/" in lien or "https://media.discordapp.net/attachments" in lien:
                url = lien
                response = requests.get(url)
                with open("data/facial/image.jpg", "wb") as file:
                    file.write(response.content)

                ImagePath = "data/facial/image.jpg"

                #
                xml = "chemin/vers/haarcascade_frontalcatface.xml"  # Chemin modifié
                catFaceCascade = cv2.CascadeClassifier(xml)
                    
                image = cv2.imread(ImagePath)
                    
                faces = catFaceCascade.detectMultiScale(image)
                    
                if len(faces) == 0:
                    await message.channel.send("[BETA] Pas de chat détecté !")
                    
                else:
                    await message.channel.send("[BETA] Chat détecté !")

                    
                    for (x, y, w, h) in faces:
                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 5)

                cv2.imwrite('data/facial/resultat.jpg',image)
                await message.channel.send(file=discord.File('data/facial/resultat.jpg'))

                os.remove('data/facial/resultat.jpg')
                os.remove('data/facial/image.jpg')
            else:
                #error me
                embed=discord.Embed()
                embed.add_field(name="❌  Echec de la commande...", value="Le lien doit commencer par https://cdn.discordapp.com/attachments/ ou  https://media.discordapp.net/attachments.", inline=False)
                await message.channel.send(embed=embed)
        else:
            #error message
            embed=discord.Embed()
            embed.add_field(name="❌  Echec de la commande...", value="Veuillez rédiger la commande comme ceci : .recognize_cat [lien]", inline=False)
            await message.channel.send(embed=embed)        

#commandes cachées
    if message.content.startswith(".poder"):
        # ID modifié
        if message.author.id == 123456789012345678:
            await message.channel.send("https://example.com/image.jpg")  # URL modifiée

    if message.content.startswith(".helpdieux"):
        # IDs modifiés
        if message.author.id == 123456789012345678 or message.author.id == 123456789012345679 or message.author.id == 123456789012345680 or message.author.id == 123456789012345681:
            await message.channel.send("**Voici la liste des commandes cachée:\n1- .poder [roxas seulement]\n2- .select_channel\n3- .send\n3- .actual_channel**")

    if message.content.startswith(".select_channel"):
        # IDs modifiés
        if message.author.id == 123456789012345678 or message.author.id == 123456789012345679 or message.author.id == 123456789012345680:
                try:
                    salon = message.content
                    salon = salon.replace(".select_channel ", "")
                    salon = int(salon)
                    salon = str(salon)
                    with open("data/secret/redirect_salon_id.txt", "w") as fichier:
                        fichier.write("")
                        fichier.write(salon)
                    await message.channel.send("Le salon a été sélectionné avec succès !")
                except ValueError:
                    await message.channel.send("Erreur, le salon ne peut pas être un texte, il faut un id.")

    if message.content.startswith(".s"):
        if not "select_channel" in message.content and not "show" in message.content and not "supp" in message.content and not "stop" in message.content and not "size" in message.content:
            # IDs modifiés
            if message.author.id == 123456789012345678 or message.author.id == 123456789012345679 or message.author.id == 123456789012345680 or message.author.id == 123456789012345681: 
                print(str(message.content))
                if not "@everyone" in str(message.content)  and not "@here" in str(message.content):  
                    text = message.content
                    text = text.replace(".s ", "") 
                    with open("data/secret/redirect_salon_id.txt", "r") as fichier:
                        channel_id = fichier.read()
                    channel_id = int(channel_id)
                    channel_id = client.get_channel(channel_id)
                    await channel_id.send(text)
            
    if message.content.startswith(".actual_channel"):
            with open("data/secret/redirect_salon_id.txt", "r") as fichier:
                    channel_id = fichier.read()
            channel_id = int(channel_id)
            channel = discord.utils.get(client.get_all_channels(), id=channel_id)
            await message.channel.send(f"Le salon actuel est {channel}")

    if message.content.startswith(".cadres"):
            # IDs modifiés
            if message.author.id == 123456789012345678 or message.author.id == 123456789012345679 or message.author.id == 123456789012345680 or message.author.id == 123456789012345681:
                await message.channel.send("https://example.com/all_in_one.jpg")  # URL modifiée

    if message.content.startswith(".code"):
            if message.author.guild_permissions.administrator == True:
                embed=discord.Embed(color=0x0008ff)
                embed.add_field(name="Voici mon code :", value="https://github.com/username/repository", inline=False)  # URL modifiée
                await message.channel.send(embed=embed)
            else:
                #error message
                embed=discord.Embed()
                embed.add_field(name="❌  Echec de la commande...", value="Cette commande nécéssite la permission administrateur.", inline=False)
                await message.channel.send(embed=embed)

    if message.content.startswith(".ping"):
            if message.author.guild_permissions.administrator == True:
                command = message.content;command = command.replace(".ping ", "")
                command = command + command + command +command +command +command +command +command +command +command
                command = command + command + command + command + command +" Cheh"

                for i in range(10):  # Réduit de 1000 à 10 pour éviter le spam excessif
                    await message.channel.send(command)
            else:
                #error message
                embed=discord.Embed()
                embed.add_field(name="❌  Echec de la commande...", value="Cette commande nécéssite la permission administrateur.", inline=False)
                await message.channel.send(embed=embed)

    if message.content.startswith(".test"):
            await message.channel.send(file=discord.File('tests/canard.jpg'))  # Chemin modifié

client.run(token)