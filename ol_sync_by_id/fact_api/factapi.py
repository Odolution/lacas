import requests

from iteration_utilities import unique_everseen

# global variable


# student_dic ={}

class Fact_Api():
    student_data_list = list()
    data = {}
    def getstudentdata(self,fact_id,page_by_page,school_name_key):
        # url = f"https://api.factsmgt.com/Students?Page={page_by_page}"
        url = f"https://api.factsmgt.com/Students?filters=studentId=={fact_id}"
        
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': school_name_key
        }

        response = requests.request("GET", url, headers=headers, data=payload).json()
        result = response['results']
        for student in result:
            self.student_data_list.append(student)
            self.data['student'] = student
            # if fact_id == student.get('studentId'):
            #     self.student_data_list.append(student)
            #     self.data['student'] = student
            #     break
                # student_dic.extend(student)


    def getpickupdata(self,fact_id, page_by_page,school_name_key):
        # url_pickup = f"https://api.factsmgt.com/students/PickupContacts?Page={page_by_page}"
        url_pickup = f"https://api.factsmgt.com/students/PickupContacts?filters=studentId=={fact_id}"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': school_name_key
        }
        response = requests.request("GET", url_pickup, headers=headers, data=payload).json()
        results = response['results']
        for pickup in results:
            self.student_data_list.append(pickup)
            self.data['pickup'] = pickup    
            # for family in family_data:
            # if fact_id == pickup.get('studentId'):
            #     self.student_data_list.append(pickup)
            #     self.data['pickup'] = pickup
            #     break


    def getpeopledata(self,fact_id, page_by_page,school_name_key):
        # url_person = f"https://api.factsmgt.com/people?Page={page_by_page}"
        url_person = f"https://api.factsmgt.com/People?filters=personId=={fact_id}"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': school_name_key
        }

        response = requests.request("GET", url_person, headers=headers, data=payload).json()
        results = response['results']
        for people in results:
            self.student_data_list.append(people)
            self.data['people'] = people
            # for student in student_data:
                # if fact_id == people.get('personId'):
                #     self.student_data_list.append(people)
                #     self.data['people'] = people
                #     break

    #
    def getpersonfamilydata(self,fact_id, page_by_page,school_name_key):
        # url_personfamily = f"https://api.factsmgt.com/people/PersonFamily?Page={page_by_page}"
        url_personfamily = f"https://api.factsmgt.com/people/PersonFamily?filters=personId=={fact_id}"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': school_name_key
        }

        response = requests.request("GET", url_personfamily, headers=headers, data=payload).json()
        results = response['results']
        fam_id = 0
        for personfamily in results:
            if 'familyId' in personfamily:
                fam_id = personfamily['familyId']
            self.student_data_list.append(personfamily)
            self.data['personfamily'] = personfamily
            # for person in poeple_data:
                # if fact_id == personfamily.get('personId'):
                #     self.student_data_list.append(personfamily)
                #     self.data['personfamily'] = personfamily
                #     break
        return fam_id

    def getfamilydata(self,person_family_data, page_by_page,school_name_key):
        url_family = f"https://api.factsmgt.com/families?Page={page_by_page}"
        url_family = f"https://api.factsmgt.com/families?api-version=1&filters=familyID=={person_family_data}"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': school_name_key
        }
        response = requests.request("GET", url_family, headers=headers, data=payload).json()
        results = response['results']
        for family in results:
            self.student_data_list.append(family)
            self.data['family']=family
                    


    def getdemographicdata(self,fact_id, page_by_page,school_name_key):
        # url_demographic = f"https://api.factsmgt.com/people/Demographic?page={page_by_page}"
        url_demographic = f"https://api.factsmgt.com/people/Demographic?filters=personId=={fact_id}"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': '9cb2c7629db3480bb42f999421d38935',
            'Facts-Api-Key': school_name_key
        }
        response = requests.request("GET", url_demographic, headers=headers, data=payload).json()
        results = response['results']
        for demo in results:
            self.student_data_list.append(demo)
            self.data['demographic']= demo
            # for personfamily in person_family_data:
                # if fact_id == demo.get('personId'):
                #     self.student_data_list.append(demo)
                #     self.data['demographic']= demo
                #     break



    def main(self,fact_id,school_name_key):
        self.getstudentdata(fact_id,0,school_name_key)
        self.getpickupdata(fact_id,0,school_name_key)
        self.getpeopledata(fact_id, 0,school_name_key)
        self.getdemographicdata(fact_id, 0,school_name_key)
        family_id = self.getpersonfamilydata(fact_id, 0,school_name_key)
        if family_id != 0:
            self.getfamilydata(family_id, 0,school_name_key)
        

        finalstudent_data_list=list(unique_everseen([i for i in self.student_data_list]))
        return self.data


#remove duplication


