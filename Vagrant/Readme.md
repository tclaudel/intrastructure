# [Vagrant](https://www.vagrantup.com/)

Création de VM, en utilisatnt des images Vagrant  
On peut aller chercher des images préfaites puis preciser avec un VagrantFile

## Commandes

- vagrant up : Download image et run toute la stack
- vagrant up <nom de la Vm> : pour lancer une seule machine
- vagrant snapshop push : faire des snapshots
- vagrant snapshot list
- vagrant snapshot pop : charger un snapshot
- vagrant halt : arreter la ou les machines
- vagrant destroy : detruire la ou les machines (-f)
- vagrant status : liste des machines
- vagrant ssh <nom de la machine. : pour acceder a la VM en CLI
- cat Vagrantfile | grep -ri ip : recuperer les ips des differentes machines

