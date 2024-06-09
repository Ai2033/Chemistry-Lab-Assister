from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
from scipy.interpolate import interp1d
import numpy as np
from tabulate import tabulate
import os
from PyInquirer import prompt
from gtts import gTTS
import subprocess
import psutil
import random
from termcolor import colored


def input_readings(dict,diff=0.5,range_=20):
    '''A function to input the readings for the lab experiments'''

    v=0.0

    for i in range(range_):
        print(v,"ml: ",end='')
        try:
            dict[v]=float(input())
        except BaseException:
            break
        
        v+=diff


def plot_graph(x_values,y_values,x_axis,y_axis):
    '''A function to plot the graph when the X and Y coordinates of the points are given'''

    x=np.array(x_values)
    y=np.array(y_values)

    spline = make_interp_spline(x, y)
    x_smooth = np.linspace(x.min(), x.max(), 500)
    y_smooth= spline(x_smooth)

    plt.plot(x_smooth,y_smooth)
    plt.scatter(x, y, color='red')
    plt.title(x_axis+" vs "+y_axis)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.show()


def tabulate_colums(data,heading,float_formats):
    '''A function to tabulate the values and form an observation table'''

    data=list(zip(*data))
    print(tabulate(data,headers=heading,tablefmt="grid",numalign="center",floatfmt=float_formats))


def text_to_speech(text,output):
    '''Converts the given text to speech by storing in an output audio file.'''
    tts = gTTS(text=text, lang='en')
    tts.save(output)
    subprocess.Popen(["afplay", output])


def terminate_process():
    """Terminates the audio."""
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if "afplay".lower() in proc.info['name'].lower():
            process = psutil.Process(proc.info['pid'])
            process.terminate()


def navigate(d,output):
    k=list(d.keys())
    v=list(d.values())

    q = [{"type":"list","name":"q","message":k[0],"choices":v[0]}]
    txt=k[0]+". "
    
    for i in v[0]:
        txt+= i +". "
        
    text_to_speech(txt,output)
    a=prompt(q)
    terminate_process()
    
    return a["q"]
    


# MAIN

d={}

while True:
    os.system('clear')
    
    txt="Chemistry Lab Experiments \n\n"
    print(colored(txt.center(163),color="magenta",attrs=["bold"]))
    
    d1={"Which lab experiment do you wish to perform?":["Conductometric titration","Potentiometric titration","Colorimetric titration","Viva Quiz"]}
    a1=navigate(d1,"output1.mp3")

    print("\n\n")

    if a1==list(d1.values())[0][0]:
        d2={"Conductometric Titration":["Strong acid against strong base","Weak acid against strong base","Mixture of strong acid and weak acid against strong base"]}
        a2=navigate(d2,"output2.mp3")
        os.system('clear')
        
        if a2==list(d2.values())[0][0]:
            #strong acid against strong base
            #d={0.0:18.24,0.5:17.54,1.0:15.72,1.5:14.56,2.0:13.31,2.5:11.98,3.0:10.89,3.5:9.35,4.0:8.07,4.5:6.56,5.0:6.43,5.5:7.10,6.0:8.27,6.5:9.16,7.0:10.08}

            txt="Conductometric Titration of strong acid against strong base \n\n"
            print(colored(txt.center(163),color="magenta",attrs=["bold"]))
            
            print("Enter the conductance value for the given Volume of NaOH :\n")
            input_readings(d)


            print("\n\nPress any key to view the observation table")
            c=input(">")

            os.system('clear')

            volume_of_NaOH=list(d.keys())
            conductance=list(d.values())

            data=[volume_of_NaOH,conductance]
            heading=["Volume of NaOH added (mL)","conductance(L)(mS)"]
            float_formats=(".1f",".2f")


            print(colored("Observation Table:\n\n",color="blue",attrs=["bold"]))
            tabulate_colums(data,heading,float_formats)


            print("\n\nPress any key to view the graphs")
            c=input(">")

            plot_graph(volume_of_NaOH,conductance,"Volume of NaOH in mL","Conductance(mS)")

            os.system('clear')

            m=conductance.index(min(conductance))

            equivalence_point=volume_of_NaOH[m]

            print(colored("Result:",color="blue",attrs=["bold"]))
            print("\nFrom the graphs, we understand that the equivalence point is :",equivalence_point,"ml ")

            print("\nEnter the volume of strong acid pipetted out:")
            v=int(input())

            print("\nEnter the concentration of NaOH in ml :")
            N=float(input())

            l=(equivalence_point*N)/v

            print(colored("\nThe Strength of strong acid is : "+str(l)+"N",color="green",attrs=["bold"]))
            print("\n\n\n")

            
            
        elif a2==list(d2.values())[0][1]:
            # Weak acid against strong base
            #d={0.0:0.8,0.5:1.3,1.0:1.8,1.5:2.4,2.0:2.9,2.5:3.3,3.0:3.8,3.5:4.3,4.0:4.7,4.5:5.2,5.0:6.3,5.5:7.6,6.0:8.9,6.5:10,7.0:11.2,7.5:12.3,8.0:13.3,8.5:14.5,9.0:15.6,9.5:16.6,10.0:17.6}

            txt="Conductometric Titration of weak acid against strong base \n\n"
            print(colored(txt.center(163),color="magenta",attrs=["bold"]))
            
            print("Enter the conductance value for the given Volume of NaOH : \n")
            input_readings(d)


            print("\n\nPress any key to view the observation table")
            c=input(">")

            os.system('clear')

            volume_of_NaOH=list(d.keys())
            conductance=list(d.values())

            data=[volume_of_NaOH,conductance]
            heading=["Volume of NaOH added (mL)","conductance(L)(mS)"]
            float_formats=(".1f",".2f")


            print(colored("Observation Table:\n\n",color="blue",attrs=["bold"]))
            tabulate_colums(data,heading,float_formats)


            print("\n\nPress any key to view the graph")
            c=input(">")

            plot_graph(volume_of_NaOH,conductance,"Volume of NaOH in mL","Conductance(mS)")

            os.system('clear')

            #Finding the equivalence and half equivalence point
            m=conductance.index(min(conductance))
            n=volume_of_NaOH.index(max(volume_of_NaOH))
            minimum=conductance[m+2]-conductance[m+1]
            for i in range(m+1,n-1,3):
                if(minimum<(conductance[i+1]-conductance[i])):
                    minimum=conductance[i+1]-conductance[i]
                    z=i-1     
            equivalence_point=volume_of_NaOH[z]
            
            print(colored("Result:",color="blue",attrs=["bold"]))
            print("\nFrom the graph, we understand that the equivalence point is :",equivalence_point,"ml")

            print("\nEnter the volume of weak acid pipetted out in ml :")
            v=int(input())

            print("\nEnter the concentertion of NaOH :")
            N=float(input())

            l=(equivalence_point*N)/v

            print(colored("\nStrength of weak acid = "+str(round(l,2))+"N",color="green",attrs=["bold"]))
            print("\n\n\n")
                
            
        else:  
            #Mixture of strong acid and weak acid against strong base
            #d={0.0:13.26,0.5:11.32,1.0:9.51,1.5:7.53,2.0:5.29,2.5:4.25,3.0:4.44,3.5:4.84,4.0:5.26,4.5:5.66,5.0:6.00,5.5:6.38,6.0:6.76,6.5:7.13,7.0:7.47,7.5:7.81,8.0:8.14,8.5:8.86,9.0:9.93,9.5:11.10,10.0:12.05}
            txt="Conductometric Titration of Mixture of strong acid and weak acid against strong base \n\n"
            print(colored(txt.center(163),color="magenta",attrs=["bold"]))
            
            print("Enter the conductance value for the given Volume of NaOH :\n")
            input_readings(d)


            print("\n\nPress any key to view the observation table")
            c=input(">")

            os.system('clear')

            volume_of_NaOH=list(d.keys())
            conductance=list(d.values())

            data=[volume_of_NaOH,conductance]
            heading=["Volume of NaOH added (mL)","conductance(L)(mS)"]
            float_formats=(".1f",".2f")


            print(colored("Observation Table:\n\n",color="blue",attrs=["bold"]))
            tabulate_colums(data,heading,float_formats)


            print("\n\nPress any key to view the graphs")
            c=input(">")

            plot_graph(volume_of_NaOH,conductance,"Volume of NaOH in mL","Conductance(S)")

            os.system('clear')

            #Finding the equivalence and half equivalence point
            m=conductance.index(min(conductance))
            n=volume_of_NaOH.index(max(volume_of_NaOH))
            equivalence_point1=volume_of_NaOH[m]
            minimum=conductance[m+2]-conductance[m+1]
            for i in range(m+1,n-1,1):
                if(minimum>(conductance[i+1]-conductance[i])):
                    minimum=conductance[i+1]-conductance[i]
                    z=i+1     
            equivalence_point2=volume_of_NaOH[z]
            
            print(colored("Result:",color="blue",attrs=["bold"]))
            print("\nFrom the graphs, we understand that the two equivalence points are :",equivalence_point1,"ml and ",equivalence_point2,"ml")

            print("\nEnter the volume of mixture of strong and weak acid pipetted out :")
            v=int(input())

            print("\nEnter the concentration of NaOH in ml :")
            N=float(input())

            l=(equivalence_point1*N)/v
            k=((equivalence_point2-equivalence_point1)*N)/v

            print(colored("\nStrength of strong acid = "+str(round(l,2))+"N",color="green",attrs=["bold"]))
            print(colored("Strength of weak acid = "+str(round(k,2))+"N",color="green",attrs=["bold"]))
            print("\n\n\n")
            
        
    elif a1==list(d1.values())[0][1]:
        
        d3={"Potentiometric titration":["Determination of pKa of vinegar using pH meter","Estimation of iron in Mohr's salt solution using standard K2Cr2O7"]}
        a3=navigate(d3,"output3.mp3")
        
        os.system('clear')
        
        if a3==list(d3.values())[0][0]:
            #Determination of pKa
            #d = {0.0:2.74,0.5:3.71,1.0:4.08,1.5:4.34,2.0:4.53,2.5:4.72,3.0:4.91,3.5:5.09,4.0:5.34,4.5:5.64,5.0:6.20,5.5:10.83,6.0:12.83,6.5:13.16,7.0:13.32,7.5:13.43}


            txt="Determination of pKa \n\n"
            print(colored(txt.center(163),color="magenta",attrs=["bold"]))

            print("Enter the ph value for the the given volume of NaOH added :\n")
            input_readings(d)

            print("\n\nPress any key to view the observation table")
            c=input(">")

            os.system('clear')

            volume_of_NaOH=list(d.keys())
            pH=list(d.values())

            delta_V=[0.0]
            delta_pH=[0.0]
            pH_by_V=[0.0]

            for i in range(len(d)-1):
                delta_V.append(0.5)
                delta_pH.append(round(pH[i+1]-pH[i],2))

            for i in range(1,len(pH)):
                pH_by_V.append(delta_pH[i]/delta_V[i])

            #Tabulating the observation table
            data=[volume_of_NaOH,pH,delta_V,delta_pH,pH_by_V]
            heading=["Volume of NaOH added (mL)","pH","ΔV","ΔpH","ΔpH/ΔV"]
            float_formats=(".1f",".2f",".1f",".2f",".2f")


            print(colored("Observation Table:\n\n",color="blue",attrs=["bold"]))
            tabulate_colums(data,heading,float_formats)


            print("\n\nPress any key to view the graphs")
            c=input(">")

            plot_graph(volume_of_NaOH,pH_by_V,"Volume of NaOH in mL","ΔpH/ΔV")
            plot_graph(volume_of_NaOH,pH,"Volume of NaOH in mL","pH")

            os.system('clear')

            #Finding the equivalence and half equivalence point
            m=pH_by_V.index(max(pH_by_V))
            equivalence_point=volume_of_NaOH[m]
            half_equivalence_point=equivalence_point/2

            print(colored("Result:",color="blue",attrs=["bold"]))
            print("\nFrom the graphs, we understand that the equivalence point is :",equivalence_point)
            print("\nHence, the half equivalence point is :",half_equivalence_point)

            #Finding the pka value for the half equivalence point by interpolating the data
            x = np.array(volume_of_NaOH)
            y = np.array(pH)

            f = interp1d(x, y, kind='linear')

            x_new = half_equivalence_point
            y_new = f(x_new)
            pka=round(float(y_new),2)


            print(colored("\n\npKa of vineger (weak acid) = "+str(pka),color="green",attrs=["bold"]))
            print("\n\n\n")
            
        else:
            #Mohr's salt
            
            #d={0:226,0.5:269,1.0:289,1.5:302,2.0:313,2.5:323,3.0:332,3.5:342,4.0:355,4.5:372,5.0:402,5.5:832,6.0:837,6.5:840,7.0:843,7.5:846,8.0:848}
            
            txt="Potentiometric Titration of FAS against Mohr's salt \n\n"
            print(colored(txt.center(163),color="magenta",attrs=["bold"]))
            
            print("Enter the potential for the the given volume of K2Cr2O7 added :\n")
            input_readings(d)

            print("\n\nPress any key to view the observation table")
            c=input(">")

            os.system('clear')

            volume_of_K2Cr2O7=list(d.keys())
            potential=list(d.values())

            delta_V=[0.0]
            delta_E=[0.0]
            E_by_V=[0.0]

            for i in range(len(d)-1):
                delta_V.append(0.5)
                delta_E.append(round(potential[i+1]-potential[i],2))

            for i in range(1,len(potential)):
                E_by_V.append(delta_E[i]/delta_V[i])

            #Tabulating the observation table
            data=[volume_of_K2Cr2O7,potential,delta_V,delta_E,E_by_V]
            heading=["Volume of K2Cr2O7 added (mL)","Potential(mV)","ΔV","ΔE","ΔE/ΔV"]
            float_formats=(".1f",".0f",".1f",".0f",".0f")


            print(colored("Observation Table:\n\n",color="blue",attrs=["bold"]))
            tabulate_colums(data,heading,float_formats)


            print("\n\nPress any key to view the graphs")
            c=input(">")

            plot_graph(volume_of_K2Cr2O7,E_by_V,"Volume of K2Cr2O7 in mL","ΔE/ΔV")

            os.system('clear')

            #Finding the equivalence
            m=E_by_V.index(max(E_by_V))
            equivalence_point=volume_of_K2Cr2O7[m]

            print(colored("Result:",color="blue",attrs=["bold"]))
            print("\nFrom the graph, volume of K2Cr2O7 at equivalence point is :",equivalence_point)
            x = np.array(volume_of_K2Cr2O7)
            y = np.array(potential)

            f = interp1d(x, y, kind='linear')

            n=(0.5*equivalence_point)/25
            w=n*392.24
            print(colored("\nNormality of FAS = "+str(n)+"N",color="green",attrs=["bold"]))
            print(colored("Weight of FAS in 1litre = "+str(round(w,2))+"g",color="green",attrs=["bold"]))
            print("\n\n\n")
            
            
    elif a1==list(d1.values())[0][2]:
        os.system('clear')
        
        #Colorimetry
        #d={0:0,5:0.07,10:0.15,15:0.22,20:0.32,'Test_solution':0.13}

        txt="Colorimetric Titration \n\n"
        print(colored(txt.center(163),color="magenta",attrs=["bold"]))
        
        print("Enter the absorbance value for the the given volume of CuS04 added :\n")
        input_readings(d,5,5) 
        Test_solution=float(input("Test solution:"))
        
        print("\n\nPress any key to view the observation table")
        c=input(">")

        os.system('clear')

        volume_of_CuSO4=np.array(list(d.keys()))
        a=list(d.values())
        absorbance=np.array(a)

        V1=[5]

        for i in range(len(d)-1):
            V1.append(5)


        #Tabulating the observation table
        data=[volume_of_CuSO4,V1,absorbance]
        heading=["Volume of standard solution of CuSO4(mL)","Volume of ammonia solution(mL)","absorbance"]
        float_formats=(".0f",".1f",".2f")


        print(colored("Observation Table:\n\n",color="blue",attrs=["bold"]))
        tabulate_colums(data,heading,float_formats)


        print("\n\nPress any key to view the graph")
        c=input(">")
        plot_graph(volume_of_CuSO4,absorbance,"Volume of CuSO4 (mL)","Absorbance")
        os.system('clear')

        x = list(np.array(volume_of_CuSO4))
        y = list(np.array(absorbance))
        V = np.interp(Test_solution,y,x)
        w=round(V*1.0221,2)
        
        print(colored("Result:",color="blue",attrs=["bold"]))
        print("\nFrom graph, Volume of test solution = ",V,"ml")
        print(colored("\nWeight of copper in the test solution = "+str(w)+"g",color="green",attrs=["bold"]))
        print("\n\n\n")


    else:
        os.system('clear')
        
        txt="Viva Quiz "
        print(colored(txt.center(163),color="magenta",attrs=["bold"]))
        
        data={
            "Which law relates the transmittance and the thickness of absorbing medium?":["Beer's law","Lambert's law","Beer-Lambert law","None of these"],
            "Which law relates the transmittance and the concentration of the coloured constituent in the solution?":["Lambert's law","Beer's law","Beer-Lambert law","None of these"],
            "What is transmittance?":["Ratio of intensity of transmitted light and intensity of incident light","Ratio of intensity of incident light and intensity of absorbed light","Ratio of intensity of transmitted light and intensity of absorbed light","Ratio of intensity of incident light and intensity of transmitted light"],
            "What is the nature of graph plotted for colorimetric titration?":["Straight line with negative slope","Parabola","Hyberbola","Straight line with positive slope"],
            "During the conductometric titration of a mixture of a weak acid and a strong acid with a strong base, what happens to the conductivity when the strong base is added to the strong acid initially?":["Conductivity increases","Conductivity decreases","Conductivity remains the same","Conductivity shows no consistent trend"],   
            "During the conductometric titration of mixture of strong acid and weak acid against strong base, what does the second equivalence point indicate?":["Neutralization point of strong acid","Neutralization point of weak acid","Neutralization point of total acid mixture","None of the above"],
            "Which of the following is true at the half-equivalence point?":["pH < pKa","pH > pKa","pH = pKa","None of the above"],
            "What are the applications of ZnO nanoparticles?":["Sunscreen creams","Lotions","Cosmetics","All of the above"],
            "The indicator electrode used in potentiometric titration is:":["Saturated calomel electrode","Platinum electrode","Silver electrode","Glass electrode"],
            "Saturated calomel electrode is a:":["Indicator electrode","Counter electrode","Primary reference electrode","Secondary reference electrode"],
            "Which ion primarily contributes to the conductivity of the solution after the equivalence point in the titration of a weak acid with a strong base?":["Hydrogen ion (H+)","Hydroxide ion (OH-)","Acetate ion (CH3COO-)","Sodium ion (Na+)"],
            "Why does the conductivity of the solution decrease initially when a weak acid is titrated with a strong base?":["The strong base neutralizes the weak acid, forming water and reducing the number of free ions","The weak acid is a poor conductor of electricity","The base is being added too slowly","The temperature of the solution decreases"],
            "At the end point, which of the following occurs:":["Fe+ gets completely converted to Fe+2","Fe+3 gets completely converted to Fe+2","Cr+3 gets completely converted to Cr+6","Fe+2 gets completely converted to Fe+3"],
            "How does the pH change when you add a small amount of strong base to a solution of acetic acid with a pH below the pKa value?":["pH increases slightly","pH decreases slightly","pH remains the same","pH increases drastically"],
            "How does the pH change at the equivalence point during the titration of acetic acid with a strong base compared to the starting pH of the acetic acid solution?":["pH decreases","pH increases","pH remains the same","pH fluctuates"],
            "What are the methods used for synthesis of nanoparticles?":["Top down","Bottom down","Top up","Both top down and bottom up"],
            "Write the correct order of conductance:":["CH3COONa > NaOH > CH3COOH","NaOH > CH3COOH > CH3COONa","Ch3COOH > NaOH > CH3COONa","NaOH > CH3COONa > CH3COOH"],
            "The reference electrode used in potentiometric titration is:":["Saturated calomel electrode","Platinum electrode","Silver electrode","Glass electrode"]
        }

        ans=[
            "Lambert's law",
            "Beer's law",
            "Ratio of intensity of transmitted light and intensity of incident light",
            "Straight line with positive slope",
            "Conductivity decreases",
            "Neutralization point of total acid mixture",
            "pH = pKa",
            "All of the above",
            "Platinum electrode",
            "Secondary reference electrode",
            "Hydroxide ion (OH-)",
            "The strong base neutralizes the weak acid, forming water and reducing the number of free ions",
            "Fe+2 gets completely converted to Fe+3",
            "pH increases slightly",
            "pH remains the same",
            "Both top down and bottom up",
            "NaOH > CH3COONa > CH3COOH",
            "Saturated calomel electrode" 
            ]
        
        score=0
        score_dict={
            0:"Uh oh, you get them all wrong. Better work harder!",
            1:"Atleast you got one right! Practice makes perfect!",
            2:"Not bad, but there's room for improvement! Keep trying!",
            3:"Halfway there! Keep it up!",
            4:"Almost made it! Just a little more effort next time!",
            5:"You nailed it! A perfect score!"}
        
        original_q=list(data.keys())
        shuffled_q=original_q.copy()
        random.shuffle(shuffled_q)
        
        for i in range(5):
            print("\n\n")
            
            questions = [{"type":"list","name":"q","message":shuffled_q[i],"choices":data[shuffled_q[i]]}]

            txt=shuffled_q[i]+"."
            for j in data[shuffled_q[i]]:
                txt+=j+","
            
            text_to_speech(txt,"output.mp3")
            
            answers=prompt(questions)
            
            terminate_process()
            
            index=original_q.index(shuffled_q[i])
            
            if answers["q"]==ans[index]:
                score+=1
            else:
                print("\nThe correct answer is :",end=" ")
                txt=colored(ans[index],color="red",attrs=["bold"])
                print(txt)
            index+=1
                
        txt=colored("\n\nYou scored : "+str(score)+"/5 \n"+score_dict[score]+"\n\n",color="green",attrs=["bold"])
        print(txt)
        
    ch=input("Do you wish to perform more experiments? (y/n) \n>")
    if ch=="y":
        continue
    else:
        print("\n\n")
        break