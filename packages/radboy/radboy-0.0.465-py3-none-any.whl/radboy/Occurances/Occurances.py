from . import *


class OccurancesUi:
	first_time_excludes=['oid','hidden','hidden_dtoe','soft_deleted','soft_deleted_dtoe','created_dtoe','modified_dtoe','modified_how_many_times_since_created']
	basic_includes=['name','type','unit_of_measure','quantity']

	group_fields=['group_name','group_uid']

	def create_new_all(self):
		with Session(ENGINE) as session:
			try:
				OCT=Occurances()
				session.add(OCT)
				session.commit()
				first_time_fields={i.name:{'default':getattr(OCT,i.name),'type':str(i.type).lower()} for i in OCT.__table__.columns if i.name not in self.first_time_excludes}
				fd=FormBuilder(data=first_time_fields)
				if fd is None:
					session.delete(OCT)
					session.commit()
					print("user backed out, nothing was saved!")
				for k in fd:
					setattr(OCT,k,fd[k])
				session.commit()
				session.refresh(OCT)
				print(std_colorize(OCT,0,1))
			except Exception as e:
				print(e)
				session.rollback()

	def create_new_basic(self):
		with Session(ENGINE) as session:
			try:
				OCT=Occurances()
				session.add(OCT)
				session.commit()
				first_time_fields={i.name:{'default':getattr(OCT,i.name),'type':str(i.type).lower()} for i in OCT.__table__.columns if i.name in self.basic_includes}
				fd=FormBuilder(data=first_time_fields)
				if fd is None:
					session.delete(OCT)
					session.commit()
					print("user backed out, nothing was saved!")
				for k in fd:
					setattr(OCT,k,fd[k])
				session.commit()
				session.refresh(OCT)
				print(std_colorize(OCT,0,1))
			except Exception as e:
				print(e)
				session.rollback()

	def edit_occurance(self):
		pass

	def lst_groups(self):
		pass

	def lst_names(self):
		pass

	def edit_groups(self):
		pass

	def delete_groups(self):
		pass

	def searchAuto(self):
		pass

	def set_max_pre(self):
		pass
	def set_min_pre(self):
		pass
	def set_min_post(self):
		pass
	def set_max_post(self):
		pass

	#hide
	def set_hidden(self):
		pass

	def set_soft_delete(self):
		pass
	def set_unit_of_measure(self):
		pass
	def set_qty(self):
		pass

	def delete(self):
		pass

	def search_select(self,rTYPE=list,display=True):
		'''Search for, select,
		display selected, or
		return selected as:
			list of Occurances
			a single Occurance
		
		'''
		with Session(ENGINE) as session:
			stext=Prompt.__init2__(None,func=FormBuilderMkText,ptext="What are you looking for?",helpText="text data to search for",data="string")
			if stext is None:
				return
			elif stext in ['d','']:
				pass

			query=session.query(Occurances)
			text_fields=[]
			text_query_fields=[]
			#setup filters for stext

			query=orderQuery(query,Occurances.created_dtoe,inverse=True)
			results=query.all()
			def display_results(results,session,query):
				pass
			if isinstance(rTYPE,list) or rType is list:
				if display:
					display_results(results,session,query)
				else:
					#list selector here
					return results
			elif isinstance(rTYPE,Occurances) or rType is Occurances:
				if display:
					display_results(results,session,query)
				else:
					pass
					#Occurance selector here
				return results
			else:
				display_results(results,session,query)

	def fix_table(self):
		Occurances.__table__.drop(ENGINE)
		Occurances.metadata.create_all(ENGINE)

	def __init__(self):
		cmds={
			uuid1():{
				'cmds':generate_cmds(startcmd=['fix','fx'],endCmd=['tbl','table']),
				'desc':"reinstall table",
				'exec':self.fix_table,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['cnw','create new','create_new','cn'],endCmd=['all','a','*','']),
				'desc':f"create new excluding fields {self.first_time_excludes}",
				'exec':self.create_new_all,
			},
			uuid1():{
				'cmds':generate_cmds(startcmd=['cnw','create new','create_new','cn'],endCmd=['basic','b','bsc','-1']),
				'desc':f"create new including fields {self.basic_includes}",
				'exec':self.create_new_basic,
			},		
		}

		htext=[]
		ct=len(cmds)
		for num,i in enumerate(cmds):
			m=f"{Fore.light_sea_green}{cmds[i]['cmds']}{Fore.orange_red_1} - {Fore.light_steel_blue}{cmds[i]['desc']}"
			msg=f"{std_colorize(m,num,ct)}"
			htext.append(msg)
		htext='\n'.join(htext)
		while True:
			doWhat=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"{self.__class__.__name__} @ Do What? ",helpText=htext,data="string")
			if doWhat is None:
				return
			elif doWhat in ['','d',]:
				print(htext)
				continue
			for i in cmds:
				if doWhat.lower() in [i.lower() for i in cmds[i]['cmds']]:
					if callable(cmds[i]['exec']):
						cmds[i]['exec']()
						break
					else:
						print(f"{i} - {cmds[i]['cmds']} - {cmds[i]['exec']}() - {cmds[i]['desc']}")
						return
