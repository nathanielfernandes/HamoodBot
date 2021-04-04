# import requests
import aiohttp
import discord
from discord.ext import commands
import os
import json
import modules.checks as checks


class Code(commands.Cog):
    """Test your big brain code `NEW`"""

    def __init__(self, bot):
        self.bot = bot
        self.language_info = json.load(
            open(f"{self.bot.filepath}/data/languageinfo.json")
        )

    async def run_code(self, ctx, language, code):
        data = {"language": language, "source": code}

        r = await self.bot.ahttp.post(
            url="https://emkc.org/api/v1/piston/execute",
            data=data,
            return_type="json",
            timeout=10,
        )
        # async with self.bot.aioSession.post(
        #     "https://emkc.org/api/v1/piston/execute", data=data
        # ) as response:
        #     r = await response.json()
        # r = requests.post("https://emkc.org/api/v1/piston/execute", data=data).json()

        if "message" not in r:
            output = (
                r["output"]
                if len(r["output"]) <= 1900
                else r["output"][:1900] + " Exceded Character Limit!"
            )

            embed = discord.Embed(
                title=f"{ctx.author}'s Code",
                description=f"**Output:** ```\n{output}```",
                color=ctx.author.color,
                timestamp=ctx.message.created_at,
            )
            embed.set_author(
                name=f"{self.language_info[r['language']]['name']} - {r['version']}",
                icon_url=self.language_info[r["language"]]["logo"],
            )
            await ctx.send(embed=embed)
        else:
            return await ctx.send("`Sorry, I couldn't run code at that moment`")

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def awk(self, ctx, *, content: commands.clean_content):
        """``awk [code]`` executes your AWK code"""
        content = content.replace("```awk", "").replace("```", "")
        await self.run_code(ctx, "awk", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def bash(self, ctx, *, content: commands.clean_content):
        """``bash [code]`` executes your Bash code"""
        content = content.replace("```bash", "").replace("```", "")
        await self.run_code(ctx, "bash", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def brainfuck(self, ctx, *, content: commands.clean_content):
        """``brainfuck [code]`` executes your Brainfuck code"""
        content = content.replace("```brainfuck", "").replace("```", "")
        await self.run_code(ctx, "brainfuck", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def c(self, ctx, *, content: commands.clean_content):
        """``c [code]`` executes your C code"""
        content = content.replace("```c", "").replace("```", "")
        await self.run_code(ctx, "c", content)

    @commands.command(aliases=["c++"])
    @checks.isAllowedCommand()
    async def cpp(self, ctx, *, content: commands.clean_content):
        """``cpp [code]`` executes your C++ code"""
        content = content.replace("```cpp", "").replace("```c++", "").replace("```", "")
        await self.run_code(ctx, "cpp", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def crystal(self, ctx, *, content: commands.clean_content):
        """``crystal [code]`` executes your Crystal code"""
        content = content.replace("```crystal", "").replace("```", "")
        await self.run_code(ctx, "crystal", content)

    @commands.command(aliases=["c#"])
    @checks.isAllowedCommand()
    async def csharp(self, ctx, *, content: commands.clean_content):
        """``csharp [code]`` executes your C# code"""
        content = (
            content.replace("```csharp", "").replace("```c#", "").replace("```", "")
        )
        await self.run_code(ctx, "csharp", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def d(self, ctx, *, content: commands.clean_content):
        """``d [code]`` executes your D code"""
        content = content.replace("```d", "").replace("```", "")
        await self.run_code(ctx, "d", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def dash(self, ctx, *, content: commands.clean_content):
        """``dash [code]`` executes your Dash code"""
        content = content.replace("```dash", "").replace("```", "")
        await self.run_code(ctx, "dash", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def elixer(self, ctx, *, content: commands.clean_content):
        """``elixer [code]`` executes your Elixer code"""
        content = content.replace("```elixer", "").replace("```", "")
        await self.run_code(ctx, "elixer", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def emacs(self, ctx, *, content: commands.clean_content):
        """``emacs [code]`` executes your Emacs code"""
        content = content.replace("```emacs", "").replace("```", "")
        await self.run_code(ctx, "emacs", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def elisp(self, ctx, *, content: commands.clean_content):
        """``elisp [code]`` executes your Elisp code"""
        content = content.replace("```elisp", "").replace("```", "")
        await self.run_code(ctx, "elisp", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def go(self, ctx, *, content: commands.clean_content):
        """``go [code]`` executes your Go code"""
        content = content.replace("```go", "").replace("```", "")
        await self.run_code(ctx, "go", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def haskell(self, ctx, *, content: commands.clean_content):
        """``haskell [code]`` executes your Haskell code"""
        content = content.replace("```haskell", "").replace("```", "")
        await self.run_code(ctx, "haskell", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def java(self, ctx, *, content: commands.clean_content):
        """``java [code]`` executes your Java code"""
        content = content.replace("```java", "").replace("```", "")
        await self.run_code(ctx, "java", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def jelly(self, ctx, *, content: commands.clean_content):
        """``jelly [code]`` executes your Jelly code"""
        content = content.replace("```jelly", "").replace("```", "")
        await self.run_code(ctx, "jelly", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def julia(self, ctx, *, content: commands.clean_content):
        """``julia [code]`` executes your Julia code"""
        content = content.replace("```julia", "").replace("```", "")
        await self.run_code(ctx, "julia", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def kotlin(self, ctx, *, content: commands.clean_content):
        """``kotlin [code]`` executes your Kotlin code"""
        content = content.replace("```kotlin", "").replace("```", "")
        await self.run_code(ctx, "kotlin", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def lisp(self, ctx, *, content: commands.clean_content):
        """``lisp [code]`` executes your Lisp code"""
        content = content.replace("```lisp", "").replace("```", "")
        await self.run_code(ctx, "lisp", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def lua(self, ctx, *, content: commands.clean_content):
        """``lua [code]`` executes your Lua code"""
        content = content.replace("```lua", "").replace("```", "")
        await self.run_code(ctx, "lua", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def nasm(self, ctx, *, content: commands.clean_content):
        """``nasm [code]`` executes your NASM code"""
        content = content.replace("```nasm", "").replace("```", "")
        await self.run_code(ctx, "nasm", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def nasm64(self, ctx, *, content: commands.clean_content):
        """``nasm64 [code]`` executes your NASM64 code"""
        content = content.replace("```nasm64", "").replace("```", "")
        await self.run_code(ctx, "nasm64", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def nim(self, ctx, *, content: commands.clean_content):
        """``nim [code]`` executes your Nim code"""
        content = content.replace("```nim", "").replace("```", "")
        await self.run_code(ctx, "nim", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def node(self, ctx, *, content: commands.clean_content):
        """``node [code]`` executes your Node code"""
        content = content.replace("```node", "").replace("```", "")
        await self.run_code(ctx, "node", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def osabie(self, ctx, *, content: commands.clean_content):
        """``osabie [code]`` executes your 05AB1E code"""
        content = content.replace("```osabie", "").replace("```", "")
        await self.run_code(ctx, "osabie", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def paradoc(self, ctx, *, content: commands.clean_content):
        """``paradoc [code]`` executes your Paradoc code"""
        content = content.replace("```paradoc", "").replace("```", "")
        await self.run_code(ctx, "paradoc", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def perl(self, ctx, *, content: commands.clean_content):
        """``perl [code]`` executes your Perl code"""
        content = content.replace("```perl", "").replace("```", "")
        await self.run_code(ctx, "perl", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def awk(self, ctx, *, content: commands.clean_content):
        """``awk [code]`` executes your AWK code"""
        content = content.replace("```awk", "").replace("```", "")
        await self.run_code(ctx, "awk", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def php(self, ctx, *, content: commands.clean_content):
        """``php [code]`` executes your PHP code"""
        content = content.replace("```php", "").replace("```", "")
        await self.run_code(ctx, "php", content)

    @commands.command(aliases=["py2"])
    @checks.isAllowedCommand()
    async def python2(self, ctx, *, content: commands.clean_content):
        """``python2 [code]`` executes your Python2 code"""
        content = (
            content.replace("```python2", "").replace("```py", "").replace("```", "")
        )
        await self.run_code(ctx, "python2", content)

    @commands.command(aliases=["py", "py3"])
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def python3(self, ctx, *, content: commands.clean_content):
        """``python3 [code]`` executes your python3 code"""
        content = (
            content.replace("```python", "").replace("```py", "").replace("```", "")
        )
        await self.run_code(ctx, "python3", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def ruby(self, ctx, *, content: commands.clean_content):
        """``ruby [code]`` executes your Ruby code"""
        content = content.replace("```ruby", "").replace("```", "")
        await self.run_code(ctx, "ruby", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def rust(self, ctx, *, content: commands.clean_content):
        """``rust [code]`` executes your Rust code"""
        content = content.replace("```rust", "").replace("```", "")
        await self.run_code(ctx, "rust", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def swift(self, ctx, *, content: commands.clean_content):
        """``swift [code]`` executes your Swift code"""
        content = content.replace("```swift", "").replace("```", "")
        await self.run_code(ctx, "swift", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def typescript(self, ctx, *, content: commands.clean_content):
        """``typescript [code]`` executes your typescript code"""
        content = content.replace("```TypeScript", "").replace("```", "")
        await self.run_code(ctx, "typescript", content)

    @commands.command()
    @checks.isAllowedCommand()
    @commands.cooldown(3, 15, commands.BucketType.channel)
    async def zip(self, ctx, *, content: commands.clean_content):
        """``zip [code]`` executes your Zip code"""
        content = content.replace("```zip", "").replace("```", "")
        await self.run_code(ctx, "zip", content)


def setup(bot):
    bot.add_cog(Code(bot))

