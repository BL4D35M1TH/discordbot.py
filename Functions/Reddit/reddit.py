import discord
from discord.ext import commands
from requests import get
from random import randint, choice
from json import dump, load

class redscrap():
    
    def post(self, subreddit):
        try:
            response = get(f"https://www.reddit.com/r/{subreddit}/hot.json?limit={randint(1, 100)}", headers={"User-agent": "Electric degenerate"})
            data = response.json()
            tmp = data['data']['children'][-1]['data']

            post = {
                "title" : tmp['title'],
                "image" : tmp['url'],
            }

            return post

        except Exception as e:
            print(f'reddit scraper ran into {e}')

class reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.scrapper = redscrap()
        with open("./Functions/Reddit/subreddits.json") as f:
            self.subreddits = load(f)

    @commands.command()
    async def reddit(self, ctx, *args):

        if (args[0] in ["add", "remove", "H"] and len(args)>1):
            
            if (args[0] == "add" and len(args)>2):
                self.subreddits[args[1]] = args[2]
            elif (args[0] == "remove"):
                self.subreddits.remove[args[1]]
            elif (args[0] == "H"):
                if (args[1] in self.subreddits['H']):
                    self.subreddits['H'].remove(args[1])
                else:
                    self.subreddits['H'].append(args[1])

            with open("./Functions/Reddit/subreddits.json", "w") as f:
                dump(self.subreddits, f, indent=4)
            
        elif (args[0] == "list"):
            await ctx.send(self.subreddits)
        

        else:
            subreddit = ""
            if (args[0] == "H"):
            
                subreddit = choice(self.subreddits['H'])

            else:

                if (args[0] in self.subreddits):
                    subreddit = self.subreddits[args[0]]
                else:
                    subreddit = args[0]

            get_post = self.scrapper.post(subreddit)

            post = discord.Embed(
                title=get_post['title'],
                colour=discord.Colour.purple()
            )
            post.set_image(url=get_post['image'])
            await ctx.send(embed=post)
        

def setup(bot):
    bot.add_cog(reddit(bot))