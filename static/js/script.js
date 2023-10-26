let boxInLeft = true;
let counter = 0;
let limit = 2;
  let boxAnimationInterval = setInterval(function(){
  counter++;
if(boxInLeft)
  {
    anime({
        targets: '.burger',
        translateX: 100,
   });
    
  }
else
  {
    anime({
  targets: '.burger',
  translateX: 0,
   }); 
  }

boxInLeft = !boxInLeft;

  if(counter==limit)
    {
      clearInterval(boxAnimationInterval);
    }
  
},1000);