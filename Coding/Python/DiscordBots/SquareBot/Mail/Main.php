<?php

declare(strict_types=1);

namespace shehab\TempRanks;

use _64FF00\PurePerms\PurePerms;
use Cassandra\Set;
use JaxkDev\DiscordBot\Bot\Discord;
use JaxkDev\DiscordBot\Plugin\Main as DiscordBot;
use JaxkDev\DiscordBot\Bot\Handlers\DiscordEventHandler;
use JaxkDev\DiscordBot\Models\Channels\ServerChannel;
use JaxkDev\DiscordBot\Models\Member;
use JaxkDev\DiscordBot\Models\Messages\Embed\Author;
use JaxkDev\DiscordBot\Models\Messages\Message;
use JaxkDev\DiscordBot\Models\Permissions\Permissions;
use JaxkDev\DiscordBot\Models\Role;
use JaxkDev\DiscordBot\Models\Webhook;
use JaxkDev\DiscordBot\Plugin\Events\DiscordBotEvent;
use JaxkDev\DiscordBot\Plugin\Events\MessageSent;
use JaxkDev\DiscordBot\Plugin\Storage;
use pocketmine\command\defaults\SaveCommand;
use pocketmine\console\ConsoleCommandSender;
use pocketmine\event\Listener;
use pocketmine\event\player\PlayerJoinEvent;
use pocketmine\event\plugin\PluginDisableEvent;
use pocketmine\permission\Permission;
use pocketmine\permission\PermissionManager;
use pocketmine\player\Player;
use pocketmine\plugin\PluginBase;
use pocketmine\command\CommandSender;
use pocketmine\command\Command;
use pocketmine\scheduler\ClosureTask;
use pocketmine\Server;
use pocketmine\utils\Config;
use pocketmine\utils\TextFormat;
use pocketmine\world\sound\BucketFillWaterSound;

class Main extends PluginBase implements Listener
{

    public PurePerms $purePerms;
    public Config $con;
    private $discord;

    public function onLoad(): void
    {
        $purePerms = $this->getServer()->getPluginManager()->getPlugin("PurePerms");
        assert($purePerms instanceof PurePerms);
        $this->purePerms = $purePerms;
        $this->con = new Config($purePerms->getDataFolder() . "players.yml", Config::YAML);
        $this->discord = $this->getServer()->getPluginManager()->getPlugin("DiscordBot");
    }

    protected function onEnable(): void
    {
        $this->getServer()->getPluginManager()->registerEvents($this, $this);
        $c = new Config($this->getDataFolder() . "config.yml", Config::YAML);
        #$this->pureperms = $this->getServer()->getPluginManager()->getPlugin("PurePerms");
        $this->purechat = $this->getServer()->getPluginManager()->getPlugin("PureChat");
        if ($c->get("data_d") == null){
            $c->set("date_d", date("d"));
            $c->save();
        }
        if ($c->get("data_m") == null){
            $c->set("date_m", date("m"));
            $c->save();
        }
        $this->Task();
    }

    public function onCommand(CommandSender $sender, Command $command, string $label, array $args): bool
    {
        $suffix_config = new Config($this->getDataFolder() . "suffixes.yml", Config::YAML);
        $joinsuffix_config = new Config($this->getDataFolder() . "joinsuffixes.yml", Config::YAML);
        $vip_config = new Config($this->getDataFolder() . "vip.yml", Config::YAML);
        $vipplus_config = new Config($this->getDataFolder() . "vipplus.yml", Config::YAML);
        $date_config = new Config($this->getDataFolder() . "date.yml", Config::YAML);
        $perms_config = new Config($this->getDataFolder() . "perms.yml", Config::YAML);
        switch ($command->getName()) {
            case "rankinfo":
                $sender = $sender->getName();
                if (isset($args[0])){
                    if (Server::getInstance()->isOp($sender)){
                        if (Server::getInstance()->getPlayerByPrefix($args[0]) == null){
                            $this->DaysLeft($sender, $args[0]);
                        } else {
                            $this->DaysLeft($sender, strtolower(Server::getInstance()->getPlayerByPrefix($args[0])->getName()));
                        }
                    } else {
                        $this->DaysLeft($sender, $sender);
                    }
                } else {
                    $this->DaysLeft(Server::getInstance()->getPlayerByPrefix($sender), $sender);
                }
                break;

            case "temp":
                if (isset($args[0])){
                    switch ($args[0]) {
                        case "loadit":
                            #$this->getPluginLoader()->loadPlugin("DiscordBot");
                            $this->getServer()->getPluginManager()->enablePlugin($this->discord);
                            break;
                        case "rank":
                            if (isset($args[1]) && isset($args[2]) && isset($args[3])){
                                if ($args[2] == "Vip" or $args[2] == "VipPlus" && is_numeric($args[3])){

                                    if (Server::getInstance()->getPlayerByPrefix($args[1]) !== null){
                                        $nm = strtolower(Server::getInstance()->getPlayerByPrefix($args[1])->getName());
                                        if ($args[2] == "Vip"){
                                            $vip_config->set(strtolower(Server::getInstance()->getPlayerByPrefix($args[1])->getName()), $vip_config->get($nm) + $args[3]);
                                            $vip_config->save();
                                            $sender->sendMessage("done setted rank vip for $nm");
                                            Server::getInstance()->dispatchCommand(new ConsoleCommandSender($this->getServer(), $this->getServer()->getLanguage()), "setrank \"$nm\" \"Vip\"");
                                            #$this->setperms(Server::getInstance()->getPlayerByPrefix($args[1]));
                                        }
                                        if ($args[2] == "VipPlus"){
                                            $vipplus_config->set(strtolower(Server::getInstance()->getPlayerByPrefix($args[1])->getName()), $vipplus_config->get($nm) + $args[3]);
                                            $vipplus_config->save();
                                            $sender->sendMessage("done setted rank VipPlus for $nm");
                                            Server::getInstance()->dispatchCommand(new ConsoleCommandSender($this->getServer(), $this->getServer()->getLanguage()), "setrank \"$nm\" \"VipPlus\"");
                                            #$this->setperms(Server::getInstance()->getPlayerByPrefix($args[1]));
                                        }
                                    } else {
                                        if ($args[2] == "Vip"){
                                            $vip_config->set($args[1], $vip_config->get($args[1]) + $args[3]);
                                            $vip_config->save();
                                            $sender->sendMessage("done setted rank vip for $args[1]");
                                            Server::getInstance()->dispatchCommand(new ConsoleCommandSender($this->getServer(), $this->getServer()->getLanguage()), "setrank \"" . $args[1] . "\" Vip");
                                        }
                                        if ($args[2] == "VipPlus"){
                                            $vipplus_config->set($args[1], $vipplus_config->get($args[1]) + $args[3]);
                                            $vipplus_config->save();
                                            $sender->sendMessage("done setted rank vip for $args[1]");
                                            Server::getInstance()->dispatchCommand(new ConsoleCommandSender($this->getServer(), $this->getServer()->getLanguage()), "setrank \"" . $args[1] . "\" VipPlus");
                                        }
                                    }
                                } else {
                                    $sender->sendMessage("/temp rank [name] [rank] [days]");
                                }
                            } else {
                                $sender->sendMessage("/temp rank [name] [rank] [days]");
                            }
                            break;
                        //================================================
                        case "suffix":
                            if (isset($args[1]) && isset($args[2]) && isset($args[3])){
                                $this->setTag($args[2], $args[1], $sender, $args[3]);
                            } else {
                                $sender->sendMessage("/temp suffix [name] [suffix] [days]");
                            }
                            break;
                        case "delsuffix":
                            if (isset($args[1]) && isset($args[2])){
                                $this->delTag($args[2], $args[1], $sender);
                            } else {
                                $sender->sendMessage("/temp delsuffix [name] [suffix]");
                            }
                            break;
                    }
                } else {
                    $sender->sendMessage("use /temp [suffix, rank]");
                }
                break;

            /*case "rankperms":
                if(isset($args[0])){
                    switch ($args[0]) {
                        case "add":
                            if(isset($args[1]) && isset($args[2])){
                                foreach ($this->pureperms->getGroups() as $rank){
                                    if($args[1] == $rank->getName()){
                                        $this->addArray($this->perms, $args[1], $args[2]);
                                        $sender->sendMessage("added to rank ($args[1]) - perm ($args[2])");
                                        $sender->sendMessage("rank perms : ".implode("- ", $this->perms->get($args[1]))."");
                                    }
                                }
                            }else{
                                $sender->sendMessage("please type a group and a perms");
                                foreach($this->pureperms->getGroups() as $group)
                                {
                                    $result[] = $group->getName();
                                }
                                $sender->sendMessage("groups: ".implode(" - ",$result));
                            }
                            break;

                        case "del":
                            if(isset($args[1]) && isset($args[2])){
                                foreach ($this->pureperms->getGroups() as $rank){
                                    if($args[1] == $rank->getName()){
                                        $this->delArray($this->perms, $args[1], $args[2]);
                                        $sender->sendMessage("deleted to rank ($args[1]) - perm ($args[2])");
                                        $sender->sendMessage("rank permissions : ".implode("- ", $this->perms->get($args[1]))."");
                                    }
                                }
                            }else{
                                $sender->sendMessage("please type a group and a permission");
                                foreach($this->pureperms->getGroups() as $group)
                                {
                                    $result[] = $group->getName();
                                }
                                $sender->sendMessage("groups: ".implode(" - ",$result));
                            }
                            break;

                        case "list":
                            if(isset($args[1])){
                                        #$sender->sendMessage("rank permissions : ".implode("\n", $this->perms->get($args[1]))."");
                                $api = $this->getServer()->getPluginManager()->getPlugin("PurePerms");
                                $group = $api->getGroup($args[1]);
                                $sender->sendMessage(implode(" - ", $group->getGroupPermissions()));
                            }else{
                                $sender->sendMessage("please type a group, use /rankperms list [group]");
                            }
                            break;
                    }
                }else{
                    $sender->sendMessage("/rankperms [add, del]");
                }
                break;*/
        }
        return true;
    }

    public function disableing(PluginDisableEvent $event)
    {
        $pl = $event->getPlugin();
        if ($pl->getName() == "DiscordBot"){
            $this->getScheduler()->scheduleDelayedTask(new ClosureTask(function () {
                if (!$this->getServer()->getPluginManager()->isPluginEnabled($this->discord)){
                    $this->getServer()->getPluginManager()->enablePlugin($this->discord);
                }
            }), 20);
        }
    }

    public function discordCMD(MessageSent $event)
    {
        $member = Storage::getMember($event->getMessage()->getAuthorId() ?? ""); //Member is not required, but preferred.
        $user_id = (($member?->getUserId()) ?? (explode(".", $event->getMessage()->getAuthorId() ?? "na.na")[1]));
        $user = Storage::getUser($user_id);
        if ($user === null){
            //shouldn't happen, but can.
            $this->getLogger()->warning("Failed to process discord message event, author user '$user_id' does not exist in local storage.");
            return;
        }
        $content = trim($event->getMessage()->getContent());
        if (strlen($content) === 0){
            //Files or other type of messages.
            $this->getLogger()->debug("Ignoring message '{$event->getMessage()->getId()}', No text content.");
            return;
        }
        $pl = Storage::getMember($event->getMessage()->getAuthorId());
        $name = $pl->getUserId();
        $id = $event->getMessage()->getChannelId();
        $args = explode(" ", $event->getMessage()->getContent());
        if (isset($args[0])){
            if ($args[0] == "&temp"){
                if ((strpos(implode(" ", $pl->getRoles()), "960281986969251914") == false)){
                    $content = ("you don`t have permission to use this command !");
                    $msg = new Message($id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    return;
                }

                if (isset($args[1])){
                    switch ($args[1]) {
                        /*case "suffix":
                            #$pl = Server::getInstance()->getPlayerByPrefix($args[2]);
                            $msg = new Message($id, null, "hi bro <@$name>");
                            $this->getDiscord()->getApi()->sendMessage($msg);
                            $roles = "";
                            foreach ($pl->getRoles() as $role) {
                                $roles .= "<@&$role>, ";
                            }
                            $msg2 = new Message($id, null, "your roles are : $roles");
                            $this->getDiscord()->getApi()->sendMessage($msg2);
                            break;*/

                        case "suffix":
                            if (isset($args[2]) && isset($args[3]) && isset($args[4])){
                                $this->setTagFromDiscord($args[3], str_replace("-", " ", $args[2]), $id, $args[4]);
                            } else {
                                $content = ("/temp suffix [name] [suffix] [days]");
                                $msg = new Message($id, null, $content);
                                $this->getDiscord()->getApi()->sendMessage($msg);
                            }
                            break;
                    }
                }
            }
        }
    }

    public function onJoin(PlayerJoinEvent $event)
    {
        $suffix_config = new Config($this->getDataFolder() . "suffixes.yml", Config::YAML);
        $joinsuffix_config = new Config($this->getDataFolder() . "joinsuffixes.yml", Config::YAML);
        $vip_config = new Config($this->getDataFolder() . "vip.yml", Config::YAML);
        $vipplus_config = new Config($this->getDataFolder() . "vipplus.yml", Config::YAML);
        $date_config = new Config($this->getDataFolder() . "date.yml", Config::YAML);
        $perms_config = new Config($this->getDataFolder() . "perms.yml", Config::YAML);
        $player = $event->getPlayer();
        $api = $this->getServer()->getPluginManager()->getPlugin("PurePerms");
        $purechat = $this->getServer()->getPluginManager()->getPlugin("PureChat");
        $group = $api->getUserDataMgr()->getGroup($player);
        Server::getInstance()->dispatchCommand(new ConsoleCommandSender($this->getServer(), $this->getServer()->getLanguage()), "setrank \"" . strtolower($player->getName()) . "\" \"" . $group . "\"");
        #$this->setperms($player);
        /*//==========================Suffixes====================
        if($joinsuffix_config->exists($player->getName()) or $joinsuffix_config->exists(strtolower($player->getName()))){
            if ($joinsuffix_config->get($player->getName()) == "SWORD" or $joinsuffix_config->get($player->getName()) == ""){
                $pp = $this->getServer()->getPluginManager()->getPlugin("PurePerms");
                #$this->purePerms->getUserDataMgr()->setNode($player, "suffix", "");
                $player->sendMessage("got it ?");
                $con = new Config($this->purePerms->getDataFolder() . "players.yml", Config::YAML);
                $n = strtolower($player->getName());
                $this->con->set("$n.suffix", "");
                $this->con->save();
                $joinsuffix_config->remove($player->getName());
                $joinsuffix_config->save();
            }
            if ($joinsuffix_config->get($player->getName()) == "BOOST" or $joinsuffix_config->get($player->getName()) == ""){
                $pp = $this->getServer()->getPluginManager()->getPlugin("PurePerms");
                $this->purePerms->getUserDataMgr()->setNode($player, "suffix", "");
                $joinsuffix_config->remove($player->getName());
                $joinsuffix_config->save();
            }
            if ($joinsuffix_config->get($player->getName()) == "KILLER" or $joinsuffix_config->get($player->getName()) == ""){
                $pp = $this->getServer()->getPluginManager()->getPlugin("PurePerms");
                $this->purePerms->getUserDataMgr()->setNode($player, "suffix", "");
                $joinsuffix_config->remove($player->getName());
                $joinsuffix_config->save();
            }
        }
        if (!$suffix_config->exists($player->getName())){
            $pp = $this->getServer()->getPluginManager()->getPlugin("PurePerms");
            $this->purePerms->getUserDataMgr()->setNode($player, "suffix", " ");
        }
        //===========================================*/
    }

    public function joinmsg(PlayerJoinEvent $event)
    {
        $player = $event->getPlayer();
        $name = strtolower($player->getName());
        $vip_config = new Config($this->getDataFolder() . "vip.yml", Config::YAML);
        $vipplus_config = new Config($this->getDataFolder() . "vipplus.yml", Config::YAML);

        if ($vipplus_config->exists($name) or $vipplus_config->exists(strtolower($name))){
            $player->sendMessage("§l§6 [" . $vipplus_config->get($name) . "] days §eleft for your Vip+ Rank");
            $player->sendTitle("§l§6" . $vipplus_config->get($name) . " days", "§eleft for your Vip+ Rank");
        }
        if ($vip_config->exists($name) or $vip_config->exists(strtolower($name))){
            $player->sendMessage("§l§6[" . $vip_config->get($name) . "] days §eleft for your Vip Rank");
            $player->sendTitle("§l§6" . $vip_config->get($name) . " days", "§eleft for your Vip Rank");
        }
    }

    public function Task()
    {
        $suffix_config = new Config($this->getDataFolder() . "suffixes.yml", Config::YAML);
        $joinsuffix_config = new Config($this->getDataFolder() . "joinsuffixes.yml", Config::YAML);
        $vip_config = new Config($this->getDataFolder() . "vip.yml", Config::YAML);
        $vipplus_config = new Config($this->getDataFolder() . "vipplus.yml", Config::YAML);
        $date = new Config($this->getDataFolder() . "date.yml", Config::YAML);
        /*$this->getScheduler()->scheduleRepeatingTask(new ClosureTask(function () use ($date, $vip_config, $vipplus_config, $suffix_config): void {
            if ($date->get("date_d") !== date("d") or $date->get("date_m") !== date("m")){
                $date->set("date_d", date("d"));
                $date->set("date_m", date("m"));
                $date->save();


                foreach ($vip_config->getAll() as $pl => $days) {
                    $vip_config->set($pl, $vip_config->get($pl) - 1);
                    $vip_config->save();
                    if ($vip_config->get($pl) <= 0){
                        $vip_config->remove($pl);
                        $vip_config->save();
                        Server::getInstance()->dispatchCommand(new ConsoleCommandSender($this->getServer(), $this->getServer()->getLanguage()), "setrank \"" . $pl . "\" guest");
                    }
                }

                foreach ($vipplus_config->getAll() as $pl => $days) {
                    $vipplus_config->set($pl, $vipplus_config->get($pl) - 1);
                    $vipplus_config->save();
                    if ($vipplus_config->get($pl) <= 0){
                        $vipplus_config->remove($pl);
                        $vipplus_config->save();
                        Server::getInstance()->dispatchCommand(new ConsoleCommandSender($this->getServer(), $this->getServer()->getLanguage()), "setrank \"" . $pl . "\" guest");
                    }
                }

                foreach ($suffix_config->getAll() as $pl => $days) {
                    if (is_numeric($suffix_config->get($pl))){
                        $suffix_config->set($pl, $suffix_config->get($pl) - 1);
                        $suffix_config->save();
                        if ($suffix_config->get($pl) <= 0){
                            $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                            $info = explode(".", $pl);
                            $tags->delTagfromlist($pl, $info[0]);
                            $suffix_config->remove($pl);
                            $suffix_config->save();
                        }
                    }
                }
            }
        }), 3600 * 100);*/
    }

    public function addArray($c, $key, $thing)
    {
        $config = $c->getAll();
        if ($c->get($key) == null){
            $c->set($key, [$thing]);
            $c->save();
        } else {
            $items = $config[$key];
            if (!in_array($thing, $items)){
                if (!is_array($items)){
                    $items = array($thing);
                } else {
                    $items[] = $thing;
                    $config[$key] = $items;
                    $c->setAll($config);
                    $c->save();
                }
            }
        }
    }


    public function delArray($c, $key, $thing)
    {
        $config = $c->getAll();
        if ($c->get($key) == null){
            $c->set($key, []);
            $c->save();
        } else {
            $words = $config[$key];
            if (is_array($words)){
                if (in_array($thing, $words)){
                    $toDel = array_search($thing, $words);
                    unset($words[$toDel]);
                    $config["words"] = $words;
                    $c->setAll($config);
                    $c->save();
                }
            } else {
                if ($c->get($key) == $thing or $c->get($key) == [$thing]){
                    $c->remove($key);
                    $c->save();
                }
            }
        }
    }

    public function DaysLeft($sender, $namee)
    {
        $vip_config = new Config($this->getDataFolder() . "vip.yml", Config::YAML);
        $vipplus_config = new Config($this->getDataFolder() . "vipplus.yml", Config::YAML);
        if (($player = Server::getInstance()->getPlayerByPrefix($namee)) == null){


            if ($vipplus_config->exists($namee) or $vipplus_config->exists(strtolower($namee))){
                $sender->sendMessage("§l§6 [" . $vipplus_config->get($namee) . "] days §eleft for your Vip+ Rank");
                $sender->sendTitle("§l§6" . $vipplus_config->get($namee) . " days", "§eleft for your Vip+ Rank");
            }

            if ($vip_config->exists($namee) or $vip_config->exists(strtolower($namee))){
                $sender->sendMessage("§l§6[" . $vip_config->get($namee) . "] days §eleft for your Vip Rank");
                $sender->sendTitle("§l§6" . $vip_config->get($namee) . " days", "§eleft for your Vip Rank");
            }


        } else {

            $namee = strtolower($player->getName());
            if ($vipplus_config->exists($namee) or $vipplus_config->exists(strtolower($namee))){
                $sender->sendMessage("§l§6 [" . $vipplus_config->get($namee) . "] days §eleft for your Vip+ Rank");
                $sender->sendTitle("§l§6" . $vipplus_config->get($namee) . " days", "§eleft for your Vip+ Rank");
            }

            if ($vip_config->exists($namee) or $vip_config->exists(strtolower($namee))){
                $sender->sendMessage("§l§6[" . $vip_config->get($namee) . "] days §eleft for your Vip+ Rank");
                $sender->sendTitle("§l§6" . $vip_config->get($namee) . " days", "§eleft for your Vip+ Rank");
            }


        }
    }

    public function setTag($args, $name, $sender, $time)
    {
        $suffix_config = new Config($this->getDataFolder() . "suffixes.yml", Config::YAML);
        if (Server::getInstance()->getPlayerByPrefix($name) !== null){//online player
            $player = Server::getInstance()->getPlayerByPrefix($name);
            $nm = strtolower($player->getName());
            $name = strtolower($player->getName());
            switch ($args) {
                case "boost":
                    //===========================BOOST================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "killer":
                    //===========================KILLER================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "sword":
                    //===========================SWORD================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "tiktok":
                    //===========================TIKTOK================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "instagram":
                    //===========================INSTAGRAM================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "youtube":
                    //===========================YOUTUBE================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "crown":
                    //===========================CROWN================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "blue_diamond":
                    //===========================BLUE-DIAMOND================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "green_diamond":
                    //===========================GREEN-DIAMOND================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;

                default:
                    $sender->sendMessage("arrays [boost, sword, killer, youtube, instagram, tiktok, crown, blue_diamond, green_diamond]");
            }
        } else {//offline player
            $player = Server::getInstance()->getPlayerByPrefix($name);
            $player = $name;
            $nm = $name;
            switch ($args) {
                case "boost":
                    //===========================BOOST================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($player, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "killer":
                    //===========================KILLER================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($player, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "sword":
                    //===========================SWORD================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($player, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "tiktok":
                    //===========================TIKTOK================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($player, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "instagram":
                    //===========================INSTAGRAM================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($name, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "youtube":
                    //===========================YOUTUBE================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($name, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "crown":
                    //===========================CROWN================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($name, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "blue_diamond":
                    //===========================BLUE-DIAMOND================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($name, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "green_diamond":
                    //===========================GREEN-DIAMOND================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($name, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;

                default:
                    $sender->sendMessage("arrays [boost, sword, killer, youtube, instagram, tiktok, crown, blue_diamond, green_diamond]");
            }
        }
    }

    public function delTag($args, $name, $sender)
    {
        $suffix_config = new Config($this->getDataFolder() . "suffixes.yml", Config::YAML);
        if (Server::getInstance()->getPlayerByPrefix($name) !== null){//online player
            $player = Server::getInstance()->getPlayerByPrefix($name);
            $nm = strtolower($player->getName());
            $name = strtolower($player->getName());
            switch ($args) {
                case "boost":
                    //===========================BOOST================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($player->getName()));
                    }
                    $tags->delTagfromlist(strtolower($player->getName()), "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "killer":
                    //===========================KILLER================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($player->getName()));
                    }
                    $tags->delTagfromlist(strtolower($player->getName()), "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "sword":
                    //===========================SWORD================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($player->getName()));
                    }
                    $tags->delTagfromlist(strtolower($player->getName()), "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "tiktok":
                    //===========================TIKTOK================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($player->getName()));
                    }
                    $tags->delTagfromlist(strtolower($player->getName()), "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "instagram":
                    //===========================INSTAGRAM================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($player->getName()));
                    }
                    $tags->delTagfromlist(strtolower($player->getName()), "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "youtube":
                    //===========================YOUTUBE================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($player->getName()));
                    }
                    $tags->delTagfromlist(strtolower($player->getName()), "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "crown":
                    //===========================CROWN================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($player->getName()));
                    }
                    $tags->delTagfromlist(strtolower($player->getName()), "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "blue_diamond":
                    //===========================BLUE-DIAMOND================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($player->getName()));
                    }
                    $tags->delTagfromlist(strtolower($player->getName()), "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;
                case "green_diamond":
                    //===========================GREEN-DIAMOND================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($player->getName()));
                    }
                    $tags->delTagfromlist(strtolower($player->getName()), "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . strtolower($player->getName()));
                    //==============================================================
                    break;

                default:
                    $sender->sendMessage("arrays [boost, sword, killer, youtube, instagram, tiktok, crown, blue_diamond, green_diamond]");
            }
        } else {//offline player
            $player = strtolower($name);
            $nm = strtolower($name);
            switch ($args) {
                case "boost":
                    //===========================BOOST================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($name));
                    }
                    $tags->delTagfromlist($player, "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "killer":
                    //===========================KILLER================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($name));
                    }
                    $tags->delTagfromlist($player, "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "sword":
                    //===========================SWORD================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($name));
                    }
                    $tags->delTagfromlist($player, "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "tiktok":
                    //===========================TIKTOK================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($name));
                    }
                    $tags->delTagfromlist($player, "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "instagram":
                    //===========================INSTAGRAM================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($name));
                    }
                    $tags->delTagfromlist($player, "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "youtube":
                    //===========================YOUTUBE================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($name));
                    }
                    $tags->delTagfromlist($player, "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "crown":
                    //===========================CROWN================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($name));
                    }
                    $tags->delTagfromlist($player, "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "blue_diamond":
                    //===========================BLUE-DIAMOND================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($name));
                    }
                    $tags->delTagfromlist($player, "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;
                case "green_diamond":
                    //===========================GREEN-DIAMOND================================
                    $tag = "";
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    if ($tags->getTag($name) == $tag){
                        $tags->delTag(strtolower($name));
                    }
                    $tags->delTagfromlist($player, "");
                    $suffix_config->remove(".$name");
                    $suffix_config->save();
                    $sender->sendMessage("done setted  to " . $name);
                    //==============================================================
                    break;

                default:
                    $sender->sendMessage("arrays [boost, sword, killer, youtube, instagram, tiktok, crown, blue_diamond, green_diamond]");
            }
        }
    }

    public function getDiscord(): DiscordBot
    {
        return $this->discord;
    }


    /*public function setperms(Player $player){
        $suffix_config = new Config($this->getDataFolder() . "suffixes.yml", Config::YAML);
        $joinsuffix_config = new Config($this->getDataFolder() . "joinsuffixes.yml", Config::YAML);
        $vip_config = new Config($this->getDataFolder() . "vip.yml", Config::YAML);
        $vipplus_config = new Config($this->getDataFolder() . "vipplus.yml", Config::YAML);
        $date_config = new Config($this->getDataFolder() . "date.yml", Config::YAML);
        $perms_config = new Config($this->getDataFolder() . "perms.yml", Config::YAML);
        $api = $this->getServer()->getPluginManager()->getPlugin("PurePerms");
        $group = $api->getUserDataMgr()->getGroup($player);
        if($group->getGroupPermissions() !== null){
            foreach ($group->getGroupPermissions() as $perm){
                if(!$player->isPermissionSet($perm)){
                    $player->setBasePermission($perm, true);
                }
            }
            $player->sendMessage("done, added the permissions to you.");
        }else{
            $player->sendMessage("wtf you have no perms please contact to the owner !");
        }
    }*/

    public function setTagFromDiscord($args, $name, $channle_id, $time)
    {
        $suffix_config = new Config($this->getDataFolder() . "suffixes.yml", Config::YAML);
        if (Server::getInstance()->getPlayerByPrefix($name) !== null){//online player
            $player = Server::getInstance()->getPlayerByPrefix($name);
            $nm = strtolower($player->getName());
            $name = strtolower($player->getName());
            switch ($args) {
                case "boost":
                    //===========================BOOST================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . strtolower($player->getName()));
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "killer":
                    //===========================KILLER================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . strtolower($player->getName()));
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "sword":
                    //===========================SWORD================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . strtolower($player->getName()));
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "tiktok":
                    //===========================TIKTOK================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . strtolower($player->getName()));
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "instagram":
                    //===========================INSTAGRAM================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . strtolower($player->getName()));
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "youtube":
                    //===========================YOUTUBE================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . strtolower($player->getName()));
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "crown":
                    //===========================CROWN================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . strtolower($player->getName()));
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "blue_diamond":
                    //===========================BLUE-DIAMOND================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . strtolower($player->getName()));
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "green_diamond":
                    //===========================GREEN-DIAMOND================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag(strtolower($player->getName()), "");
                    $tags->addTag(strtolower($player->getName()), "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . strtolower($player->getName()));
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;

                default:
                    $content = ("arrays [boost, sword, killer, youtube, instagram, tiktok, crown, blue_diamond, green_diamond]");
            }
        } else {//offline player
            $player = Server::getInstance()->getPlayerByPrefix($name);
            $player = $name;
            $nm = $name;
            switch ($args) {
                case "boost":
                    //===========================BOOST================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($player, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . $name);
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "killer":
                    //===========================KILLER================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($player, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . $name);
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "sword":
                    //===========================SWORD================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($player, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . $name);
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "tiktok":
                    //===========================TIKTOK================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($player, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . $name);
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "instagram":
                    //===========================INSTAGRAM================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($name, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . $name);
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "youtube":
                    //===========================YOUTUBE================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($name, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . $name);
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "crown":
                    //===========================CROWN================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($name, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . $name);
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "blue_diamond":
                    //===========================BLUE-DIAMOND================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($name, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . $name);
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;
                case "green_diamond":
                    //===========================GREEN-DIAMOND================================
                    $tags = $this->getServer()->getPluginManager()->getPlugin("TAGS");
                    $tags->setTag($name, "");
                    $tags->addTag($player, "");
                    $suffix_config->set(".$name", $time);
                    $suffix_config->save();
                    $content = ("done setted  to " . $name);
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
                    //==============================================================
                    break;

                default:
                    $content = ("arrays [boost, sword, killer, youtube, instagram, tiktok, crown, blue_diamond, green_diamond]");
                    $msg = new Message($channle_id, null, $content);
                    $this->getDiscord()->getApi()->sendMessage($msg);
            }
        }
    }
}