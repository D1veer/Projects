<?php

$suffix = ["&temp", "suffix", "boost", "sword", "killer", "youtube", "instagram", "tiktok", "crown", "blue_diamond", "green_diamond"]
case "suffix":
  if (isset($args[2]) && isset($args[3]) && isset($args[4])){
    foreach ($args as $name) {
      if ($name in_array($name, $suffixs)) {} else {
        $fullname = "";
        $fullname .= " ".$name;
      } 
    }
    $this->setTagFromDiscord($args[3], $fullname, $id, $args[4]);
  } else {
    $content = ("/temp suffix [name] [suffix] [days]");
    $msg = new Message($id, null, $content);
    $this->getDiscord()->getApi()->sendMessage($msg);
  }
  break;
?>