Using `mermaid` to create flowcharts.
See documentation at: https://mermaid-js.github.io/mermaid/#/flowchart

By using diagram tools like `mermaid`:
* modifications to flowcharts do not have to be re-uploaded with images every time.
* the markdown syntax is intuitive. 

However, `mermaid` sometimes cannot 100% recreate the desired graphs. Work-arounds may be necessary (see difference of the flowchart below and `data_process_flow.png`).

## Data processing flow diagram
A sample recreation of the data processing flow enclosed in this directory:

```mermaid
flowchart TB
    subgraph ID100[ ]
        ID1[BRFSS 2014 \n n=464,664]==>ID2[Veteran \n n=61,120]
        ID2==>ID3[Known diabetes status \n n=62,104]
        ID3==>ID4[Known asthma status \n n=61,833]
        ID4==>ID5[Known average sleep per night \n n=61,08]
    end
ID1-->ID10[Not a Veteran \n n=402,544]
ID2-->ID11[No information \n on diabetes status \n n=106]
ID3-->ID12[No asthma \nstatus \n n=181]
ID4-->ID13[No information \n average sleep \n per night \n n=752]
```

## Data integration diagram
```mermaid
flowchart LR
    %% creating nodes
    id1([Data \n Integration])
    
    %% linking nodes
    id2((External \n Applications))-->id1
    id3[(\nData Services)]-->id1
    id4((Enterprise \n Applications))-->id1
    id5(Unstructured Files)-->id1
    id6[[Cloud Applications \n and Databases]]-->id1
    
    %% integration to warehouse
    id1-->id7[(\n\n Enterprise Data \n Warehouse \n\n)]
```
