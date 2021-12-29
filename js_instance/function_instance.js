const instance = () => {
	
	

				var all_objects=m_scs.get_all_objects();
				//document.getElementById("obj").innerHTML="obj="+all_objects.length;
				var test=[];var I1=0;
				for (var i = 0; i < (all_objects.length)-1; i++) {if (m_obj_util.is_empty(all_objects[i])){test.push(all_objects[i])};};
				//document.getElementById("obj_empty").innerHTML="empty="+test.length;
				
				
				
				for (var is = 0; is < test.length; is++) {
					var instance = test[is].name;
					//r�initialise le nom
					var source="";
					//supprime les 9 derniers caracteres correspondant � _inst.001,002...etc
					for (var i = 0; i< instance.length-9; i++) {source=source.concat(instance.charAt(i));};
					
					try{
						//capture l'objet
						var source_obj = m_scs.get_object_by_name(source);
						//Attrape l'objet qui conserve les materiaux � modifier.
						var index_mat = m_scs.get_object_by_name("Index_mat");
						
						//copie l'objet
						var new_obj = m_obj.copy(source_obj, source+"_" + I1.toString(), false);
						I1++;
						
						check_mat(index_mat,new_obj);//test et modifie la couleur de certain materiaux
						
						//enregistre la position de l'instance en cours
						var pos = m_trans.get_translation(m_scs.get_object_by_name(instance));
						//enregistre la rotation de l'instance en cours
						var rot = m_trans.get_rotation(m_scs.get_object_by_name(instance));
						//enregistre le scale de l'instance en cours
						var sca = m_trans.get_scale(m_scs.get_object_by_name(instance));
						//translate l'objet dessus
						m_scs.append_object(new_obj);
						//applique la translation	
						var x=pos[0],y =pos[1],z = pos[2];
						m_trans.set_translation(new_obj,x,y,z);
						//applique le scale
						var sx=sca[0],sy=sca[1],sz=sca[2];
						//m_trans.set_scale(new_obj,sx,sy,sz);
						//applique la rotation
						var rx=rot[0],ry=rot[1],rz=rot[2],rw=rot[3];
						m_trans.set_rotation(new_obj,rx,ry,rz,rw);
						}catch(error){console.error(error);}
					
					
					//attache le mouvement de la copie � sa source
				};
					
			
	
};